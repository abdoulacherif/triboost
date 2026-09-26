from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# HELPER : VÉRIFIER ACTIVATION
# ============================================================
async def _check_activated(request: Request):
    """Vérifie que l'utilisateur est connecté ET activé."""
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
        raise HTTPException(
            status_code=403,
            detail="Compte non activé. Activez pour 3 600 FCFA pour accéder aux parcours."
        )

    return user.user.id


# ============================================================
# LISTER LES PARCOURS (accessible à tous les connectés)
# ============================================================
@router.get("/paths")
async def list_paths(request: Request):
    try:
        admin = get_supabase_admin()
        paths_result = admin.table("paths").select("*").eq("is_active", True).order("sort_order").execute()
        paths = paths_result.data or []

        auth_header = request.headers.get("Authorization", "")
        user_id = None
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                user = get_supabase().auth.get_user(token)
                if user.user:
                    user_id = user.user.id
            except Exception:
                pass

        for p in paths:
            chapters = admin.table("course_chapters").select("id").eq("path_id", p["id"]).execute()
            chapter_ids = [c["id"] for c in (chapters.data or [])]
            p["chapters_count"] = len(chapter_ids)

            lessons_count = 0
            if chapter_ids:
                lessons = admin.table("course_lessons").select("id").in_("chapter_id", chapter_ids).execute()
                lessons_count = len(lessons.data or [])
            p["lessons_count"] = lessons_count

            p["is_unlocked"] = False
            p["completed_lessons"] = 0
            if user_id:
                unlock = admin.table("path_unlocks").select("*").eq("user_id", user_id).eq("path_id", p["id"]).execute()
                if unlock.data and len(unlock.data) > 0:
                    p["is_unlocked"] = True
                    p["unlock_data"] = unlock.data[0]
                    prog = admin.table("lesson_progress").select("id").eq("user_id", user_id).eq("unlock_id", unlock.data[0]["id"]).execute()
                    p["completed_lessons"] = len(prog.data or [])

        return {"success": True, "paths": paths}
    except Exception as e:
        print(f"[COURSES] paths: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# DÉTAIL D'UN PARCOURS (accessible à tous les connectés)
# ============================================================
@router.get("/paths/{path_id}")
async def get_path_detail(path_id: str, request: Request):
    try:
        admin = get_supabase_admin()

        path = admin.table("paths").select("*").eq("id", path_id).eq("is_active", True).execute()
        if not path.data or len(path.data) == 0:
            raise HTTPException(status_code=404, detail="Parcours introuvable")

        p = path.data[0]

        chapters_result = admin.table("course_chapters").select("*").eq("path_id", path_id).order("sort_order").execute()
        chapters = chapters_result.data or []

        for ch in chapters:
            lessons = admin.table("course_lessons").select(
                "id, title, content, content_url, day_number, gain_amount, loss_amount, sort_order"
            ).eq("chapter_id", ch["id"]).order("sort_order").execute()
            ch["lessons"] = lessons.data or []

        p["chapters"] = chapters

        auth_header = request.headers.get("Authorization", "")
        user_id = None
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                user = get_supabase().auth.get_user(token)
                if user.user:
                    user_id = user.user.id
            except Exception:
                pass

        p["is_unlocked"] = False
        p["completed_lesson_ids"] = []
        p["last_day"] = 0
        p["total_gained"] = 0
        p["total_lost"] = 0

        if user_id:
            unlock = admin.table("path_unlocks").select("*").eq("user_id", user_id).eq("path_id", path_id).execute()
            if unlock.data and len(unlock.data) > 0:
                u = unlock.data[0]
                p["is_unlocked"] = True
                p["unlock_data"] = u
                p["total_gained"] = float(u.get("total_gained", 0))
                p["total_lost"] = float(u.get("total_lost", 0))

                prog = admin.table("lesson_progress").select("lesson_id, day_number").eq("user_id", user_id).eq("unlock_id", u["id"]).execute()
                p["completed_lesson_ids"] = [x["lesson_id"] for x in (prog.data or [])]

                days = [x["day_number"] for x in (prog.data or [])]
                p["last_day"] = max(days) if days else 0

        return {"success": True, "path": p}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[COURSES] path detail: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# DÉBLOQUER UN PARCOURS (⚠️ COMPTE ACTIVÉ REQUIS)
# ============================================================
@router.post("/paths/{path_id}/unlock")
async def unlock_path(path_id: str, request: Request):
    try:
        user_id = await _check_activated(request)
        admin = get_supabase_admin()

        result = admin.rpc("unlock_path", {
            "p_user_id": user_id,
            "p_path_id": path_id,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# RÉCUPÉRER LES QUESTIONS (⚠️ COMPTE ACTIVÉ REQUIS)
# ============================================================
@router.get("/lessons/{lesson_id}/questions")
async def get_lesson_questions(lesson_id: str, request: Request):
    try:
        user_id = await _check_activated(request)
        admin = get_supabase_admin()

        lesson = admin.table("course_lessons").select("*").eq("id", lesson_id).execute()
        if not lesson.data:
            raise HTTPException(status_code=404, detail="Leçon introuvable")

        lesson_data = lesson.data[0]
        chapter = admin.table("course_chapters").select("path_id").eq("id", lesson_data["chapter_id"]).execute()
        if not chapter.data:
            raise HTTPException(status_code=404, detail="Chapitre introuvable")

        path_id = chapter.data[0]["path_id"]

        unlock = admin.table("path_unlocks").select("id").eq("user_id", user_id).eq("path_id", path_id).execute()
        if not unlock.data or len(unlock.data) == 0:
            raise HTTPException(status_code=403, detail="Parcours non débloqué")

        already = admin.table("lesson_progress").select("id").eq("user_id", user_id).eq("lesson_id", lesson_id).execute()
        if already.data and len(already.data) > 0:
            raise HTTPException(status_code=400, detail="Leçon déjà terminée")

        questions = admin.table("lesson_questions").select("id, question, options, sort_order").eq("lesson_id", lesson_id).order("sort_order").execute()

        return {
            "success": True,
            "lesson": {
                "id": lesson_data["id"],
                "title": lesson_data["title"],
                "content": lesson_data["content"],
                "content_url": lesson_data.get("content_url", ""),
                "day_number": lesson_data["day_number"],
                "gain_amount": lesson_data["gain_amount"],
                "loss_amount": lesson_data["loss_amount"],
            },
            "questions": questions.data or [],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SOUMETTRE LES RÉPONSES (⚠️ COMPTE ACTIVÉ REQUIS)
# ============================================================
@router.post("/lessons/{lesson_id}/submit")
async def submit_answers(lesson_id: str, request: Request):
    try:
        user_id = await _check_activated(request)
        admin = get_supabase_admin()

        body = await request.json()
        answers = body.get("answers", {})

        result = admin.rpc("submit_lesson_answers", {
            "p_user_id": user_id,
            "p_lesson_id": lesson_id,
            "p_answers": answers,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))