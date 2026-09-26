import secrets

from fastapi import APIRouter, HTTPException, Request, Header

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# VÉRIFICATION UTILISATEUR CONNECTÉ + ACTIVÉ
# ============================================================
async def _check_user(request: Request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")

    token = auth_header.replace("Bearer ", "")
    user = get_supabase().auth.get_user(token)
    if not user.user:
        raise HTTPException(status_code=401, detail="Token invalide")

    admin = get_supabase_admin()
    profile = admin.table("profiles").select("is_activated").eq("id", user.user.id).execute()
    raw = profile.data[0].get("is_activated") if profile.data else False
    is_activated = raw is True or raw == "true" or raw == 1 or raw == "1"

    if not is_activated:
        raise HTTPException(status_code=403, detail="Compte non activé")

    return user.user.id


# ============================================================
# CONTENU COMPLET D'UNE LEÇON
# ============================================================
@router.get("/lesson/{lesson_id}")
async def get_lesson_full(lesson_id: str, request: Request):
    try:
        user_id = await _check_user(request)
        admin = get_supabase_admin()

        lesson = admin.table("course_lessons").select("*").eq("id", lesson_id).execute()
        if not lesson.data:
            raise HTTPException(status_code=404, detail="Leçon introuvable")

        l = lesson.data[0]
        chapter = admin.table("course_chapters").select("id, title, path_id").eq("id", l["chapter_id"]).execute()
        ch = chapter.data[0] if chapter.data else {}

        # Vérifier déblocage
        unlock = admin.table("path_unlocks").select("*").eq("user_id", user_id).eq("path_id", ch.get("path_id")).execute()
        if not unlock.data or len(unlock.data) == 0:
            raise HTTPException(status_code=403, detail="Parcours non débloqué")

        u = unlock.data[0]

        # Vérifier la règle 24h
        next_at = u.get("next_lesson_available_at")
        can_start = True
        remaining_seconds = 0

        if next_at:
            from datetime import datetime, timezone
            try:
                next_dt = datetime.fromisoformat(next_at.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                if now < next_dt:
                    can_start = False
                    remaining_seconds = int((next_dt - now).total_seconds())
            except Exception:
                pass

        # Blocs de contenu
        blocks = admin.table("lesson_content_blocks").select("*").eq("lesson_id", lesson_id).order("sort_order").execute()

        # Exercices
        exercises = admin.table("lesson_exercises").select("id, title, instructions, exercise_type, options, points, sort_order").eq("lesson_id", lesson_id).order("sort_order").execute()

        # Déjà terminée ?
        already_done = admin.table("lesson_progress").select("id").eq("user_id", user_id).eq("lesson_id", lesson_id).execute()
        is_done = bool(already_done.data)

        return {
            "success": True,
            "lesson": {
                "id": l["id"],
                "title": l["title"],
                "content": l.get("content", ""),
                "video_url": l.get("video_url", ""),
                "pdf_url": l.get("pdf_url", ""),
                "cover_url": l.get("cover_url", ""),
                "objectives": l.get("objectives", ""),
                "duration_minutes": l.get("duration_minutes", 30),
                "day_number": l["day_number"],
                "gain_amount": l["gain_amount"],
                "loss_amount": l["loss_amount"],
            },
            "chapter": {"id": ch.get("id"), "title": ch.get("title", "")},
            "can_start": can_start and not is_done,
            "remaining_seconds": remaining_seconds,
            "is_done": is_done,
            "blocks": blocks.data or [],
            "exercises": exercises.data or [],
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[LESSON] {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# DÉMARRER LA SESSION (timer)
# ============================================================
@router.post("/lesson/{lesson_id}/start")
async def start_session(lesson_id: str, request: Request):
    try:
        user_id = await _check_user(request)
        admin = get_supabase_admin()

        result = admin.rpc("start_lesson_session", {
            "p_user_id": user_id,
            "p_lesson_id": lesson_id,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# TERMINER LA SESSION
# ============================================================
@router.post("/lesson/{lesson_id}/finish")
async def finish_session(lesson_id: str, request: Request):
    try:
        user_id = await _check_user(request)
        body = await request.json()
        session_id = body.get("session_id")
        answers = body.get("answers", {})

        if not session_id:
            raise HTTPException(status_code=400, detail="Session manquante")

        admin = get_supabase_admin()

        result = admin.rpc("finish_lesson_session", {
            "p_user_id": user_id,
            "p_session_id": session_id,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        if not result.data.get("success"):
            return {"success": True, "result": result.data}

        # Corriger les exercices
        lesson = admin.table("course_lessons").select("*").eq("id", lesson_id).execute()
        l = lesson.data[0]

        exercises = admin.table("lesson_exercises").select("id, correct_answer, points").eq("lesson_id", lesson_id).execute()
        total_points = 0
        earned_points = 0

        for ex in (exercises.data or []):
            total_points += ex.get("points", 100)
            user_ans = (answers.get(ex["id"]) or "").strip().lower()
            correct = (ex.get("correct_answer") or "").strip().lower()
            if user_ans == correct:
                earned_points += ex.get("points", 100)

        # Appliquer les gains (déjà gérés dans submit_lesson_answers)
        # On utilise la même fonction
        admin.rpc("submit_lesson_answers", {
            "p_user_id": user_id,
            "p_lesson_id": lesson_id,
            "p_answers": answers,
        }).execute()

        return {"success": True, "result": result.data, "score": {"earned": earned_points, "total": total_points}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# API EXTERNE — RÉCUPÉRER UNE LEÇON VIA API KEY
# ============================================================
@router.get("/external/lesson/{lesson_id}")
async def external_get_lesson(lesson_id: str, x_api_key: str = Header(None)):
    try:
        if not x_api_key:
            raise HTTPException(status_code=401, detail="API key manquante")

        admin = get_supabase_admin()
        key = admin.table("platform_api_keys").select("*").eq("api_key", x_api_key).eq("is_active", True).execute()

        if not key.data or len(key.data) == 0:
            raise HTTPException(status_code=401, detail="API key invalide")

        # Rate limit
        k = key.data[0]
        if k.get("calls_today", 0) >= k.get("rate_limit_per_day", 1000):
            raise HTTPException(status_code=429, detail="Limite quotidienne atteinte")

        admin.table("platform_api_keys").update({
            "calls_today": (k.get("calls_today", 0) or 0) + 1,
            "last_call_at": "now()",
        }).eq("id", k["id"]).execute()

        # Retourner la leçon
        lesson = admin.table("course_lessons").select(
            "id, title, content, video_url, pdf_url, objectives, duration_minutes, day_number, gain_amount, loss_amount"
        ).eq("id", lesson_id).execute()

        if not lesson.data:
            raise HTTPException(status_code=404, detail="Leçon introuvable")

        blocks = admin.table("lesson_content_blocks").select("*").eq("lesson_id", lesson_id).order("sort_order").execute()
        exercises = admin.table("lesson_exercises").select("*").eq("lesson_id", lesson_id).order("sort_order").execute()

        return {
            "success": True,
            "lesson": lesson.data[0],
            "blocks": blocks.data or [],
            "exercises": exercises.data or [],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# ADMIN — GÉNÉRER UNE CLÉ API
# ============================================================
@router.post("/admin/api-keys")
async def create_api_key(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        check = admin.table("profiles").select("is_admin").eq("id", user.user.id).execute()
        if not check.data or not check.data[0].get("is_admin"):
            raise HTTPException(status_code=403, detail="Non autorisé")

        body = await request.json()
        name = (body.get("name") or "").strip()
        email = (body.get("owner_email") or "").strip()

        if not name:
            raise HTTPException(status_code=400, detail="Nom obligatoire")

        api_key = "tb_" + secrets.token_urlsafe(32)

        result = admin.table("platform_api_keys").insert({
            "name": name,
            "api_key": api_key,
            "owner_email": email,
            "is_active": True,
        }).execute()

        return {"success": True, "api_key": api_key, "data": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# ADMIN — LISTER LES CLÉS API
# ============================================================
@router.get("/admin/api-keys")
async def list_api_keys(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        check = admin.table("profiles").select("is_admin").eq("id", user.user.id).execute()
        if not check.data or not check.data[0].get("is_admin"):
            raise HTTPException(status_code=403, detail="Non autorisé")

        keys = admin.table("platform_api_keys").select("*").order("created_at", desc=True).execute()
        return {"success": True, "keys": keys.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))