import secrets

from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


async def _check_admin(request: Request) -> str:
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
    return user.user.id


# ============================================================
# PARCOURS — LISTER
# ============================================================
@router.get("/paths")
async def admin_list_paths(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.table("paths").select("*").order("sort_order").execute()
        return {"success": True, "paths": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/paths/{path_id}/update")
async def admin_update_path(path_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        update_data = {}
        for f in ["title", "description", "icon", "color"]:
            if f in body:
                update_data[f] = body[f]
        for f in ["unlock_price", "final_bonus", "reward_per_formation"]:
            if f in body:
                update_data[f] = float(body[f])
        if "total_days" in body:
            update_data["total_days"] = int(body["total_days"])
        if "is_active" in body:
            update_data["is_active"] = bool(body["is_active"])

        if update_data:
            admin.table("paths").update(update_data).eq("id", path_id).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# CHAPITRES
# ============================================================
@router.get("/paths/{path_id}/chapters")
async def list_chapters(path_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        chapters = admin.table("course_chapters").select("*").eq("path_id", path_id).order("sort_order").execute()

        for ch in (chapters.data or []):
            lessons = admin.table("course_lessons").select("*").eq("chapter_id", ch["id"]).order("sort_order").execute()
            ch["lessons"] = lessons.data or []
            for l in ch["lessons"]:
                q = admin.table("lesson_questions").select("*").eq("lesson_id", l["id"]).order("sort_order").execute()
                l["questions"] = q.data or []
                b = admin.table("lesson_content_blocks").select("*").eq("lesson_id", l["id"]).order("sort_order").execute()
                l["blocks"] = b.data or []
                ex = admin.table("lesson_exercises").select("*").eq("lesson_id", l["id"]).order("sort_order").execute()
                l["exercises"] = ex.data or []

        return {"success": True, "chapters": chapters.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/chapters/create")
async def create_chapter(request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        if not body.get("path_id") or not body.get("title"):
            raise HTTPException(status_code=400, detail="Champs obligatoires")

        result = admin.table("course_chapters").insert({
            "path_id": body["path_id"],
            "title": body["title"],
            "description": body.get("description", ""),
            "sort_order": int(body.get("sort_order", 0)),
        }).execute()

        return {"success": True, "chapter": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/chapters/{chapter_id}/update")
async def update_chapter(chapter_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        update_data = {}
        for f in ["title", "description"]:
            if f in body:
                update_data[f] = body[f]
        if "sort_order" in body:
            update_data["sort_order"] = int(body["sort_order"])

        if update_data:
            admin.table("course_chapters").update(update_data).eq("id", chapter_id).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/chapters/{chapter_id}")
async def delete_chapter(chapter_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("course_chapters").delete().eq("id", chapter_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# LEÇONS
# ============================================================
@router.post("/lessons/create")
async def create_lesson(request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        if not body.get("chapter_id") or not body.get("title"):
            raise HTTPException(status_code=400, detail="Champs obligatoires")

        result = admin.table("course_lessons").insert({
            "chapter_id": body["chapter_id"],
            "title": body["title"],
            "content": body.get("content", ""),
            "content_url": body.get("content_url", ""),
            "video_url": body.get("video_url", ""),
            "pdf_url": body.get("pdf_url", ""),
            "cover_url": body.get("cover_url", ""),
            "objectives": body.get("objectives", ""),
            "duration_minutes": int(body.get("duration_minutes", 30)),
            "day_number": int(body.get("day_number", 1)),
            "gain_amount": float(body.get("gain_amount", 50)),
            "loss_amount": float(body.get("loss_amount", 20)),
            "sort_order": int(body.get("sort_order", 0)),
        }).execute()

        return {"success": True, "lesson": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/lessons/{lesson_id}/update")
async def update_lesson(lesson_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        update_data = {}
        for f in ["title", "content", "content_url", "video_url", "pdf_url", "cover_url", "objectives"]:
            if f in body:
                update_data[f] = body[f]
        for f in ["duration_minutes", "day_number", "sort_order"]:
            if f in body:
                update_data[f] = int(body[f])
        for f in ["gain_amount", "loss_amount"]:
            if f in body:
                update_data[f] = float(body[f])

        if update_data:
            admin.table("course_lessons").update(update_data).eq("id", lesson_id).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/lessons/{lesson_id}")
async def delete_lesson(lesson_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("course_lessons").delete().eq("id", lesson_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# BLOCS DE CONTENU
# ============================================================
@router.post("/lessons/{lesson_id}/blocks/create")
async def create_block(lesson_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        result = admin.table("lesson_content_blocks").insert({
            "lesson_id": lesson_id,
            "block_type": body.get("block_type", "text"),
            "title": body.get("title", ""),
            "content": body.get("content", ""),
            "media_url": body.get("media_url", ""),
            "sort_order": int(body.get("sort_order", 0)),
        }).execute()

        return {"success": True, "block": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/blocks/{block_id}")
async def delete_block(block_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("lesson_content_blocks").delete().eq("id", block_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# EXERCICES
# ============================================================
@router.post("/lessons/{lesson_id}/exercises/create")
async def create_exercise(lesson_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        result = admin.table("lesson_exercises").insert({
            "lesson_id": lesson_id,
            "title": body.get("title", ""),
            "instructions": body.get("instructions", ""),
            "exercise_type": body.get("exercise_type", "text"),
            "correct_answer": body.get("correct_answer", ""),
            "options": body.get("options", []),
            "points": int(body.get("points", 100)),
            "sort_order": int(body.get("sort_order", 0)),
        }).execute()

        return {"success": True, "exercise": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/exercises/{exercise_id}")
async def delete_exercise(exercise_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("lesson_exercises").delete().eq("id", exercise_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# QUESTIONS (QCM)
# ============================================================
@router.post("/lessons/{lesson_id}/questions/create")
async def create_question(lesson_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        result = admin.table("lesson_questions").insert({
            "lesson_id": lesson_id,
            "question": body.get("question", ""),
            "options": body.get("options", []),
            "correct_index": int(body.get("correct_index", 0)),
            "sort_order": int(body.get("sort_order", 0)),
        }).execute()

        return {"success": True, "question": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/questions/{question_id}")
async def delete_question(question_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("lesson_questions").delete().eq("id", question_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# PROGRESSION UTILISATEURS
# ============================================================
@router.get("/progress")
async def admin_view_progress(request: Request, path_id: str = None):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        # Tous les unlocks (ou ceux d'un parcours spécifique)
        q = admin.table("path_unlocks").select("*, profiles:user_id(full_name, phone), paths:path_id(title, icon)")
        if path_id:
            q = q.eq("path_id", path_id)
        unlocks = q.order("started_at", desc=True).limit(100).execute()

        result = []
        for u in (unlocks.data or []):
            user_id = u["user_id"]

            # Progression dans ce parcours
            prog = admin.table("lesson_progress").select("lesson_id, day_number, correct_answers, total_questions, gain, loss, completed_at").eq("user_id", user_id).eq("unlock_id", u["id"]).order("completed_at", desc=True).execute()

            # Sessions
            sessions = admin.table("lesson_sessions").select("lesson_id, started_at, completed_at, elapsed_seconds, is_finished").eq("user_id", user_id).order("started_at", desc=True).limit(50).execute()

            result.append({
                "user": u.get("profiles") or {},
                "path": u.get("paths") or {},
                "unlock": {
                    "id": u["id"],
                    "amount_paid": u.get("amount_paid"),
                    "total_gained": u.get("total_gained"),
                    "total_lost": u.get("total_lost"),
                    "is_completed": u.get("is_completed"),
                    "started_at": u.get("started_at"),
                    "next_lesson_available_at": u.get("next_lesson_available_at"),
                },
                "lessons_completed": len(prog.data or []),
                "progress": prog.data or [],
                "sessions": sessions.data or [],
            })

        return {"success": True, "data": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# API KEYS EXTERNES
# ============================================================
@router.get("/api-keys")
async def list_api_keys(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        keys = admin.table("platform_api_keys").select("*").order("created_at", desc=True).execute()
        return {"success": True, "keys": keys.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api-keys/create")
async def create_api_key(request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        name = (body.get("name") or "").strip()
        if not name:
            raise HTTPException(status_code=400, detail="Nom obligatoire")

        api_key = "tb_" + secrets.token_urlsafe(32)

        result = admin.table("platform_api_keys").insert({
            "name": name,
            "api_key": api_key,
            "owner_email": body.get("owner_email", ""),
            "rate_limit_per_day": int(body.get("rate_limit_per_day", 1000)),
            "is_active": True,
        }).execute()

        return {"success": True, "api_key": api_key, "data": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/api-keys/{key_id}")
async def delete_api_key(key_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("platform_api_keys").delete().eq("id", key_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api-keys/{key_id}/toggle")
async def toggle_api_key(key_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        current = admin.table("platform_api_keys").select("is_active").eq("id", key_id).execute()
        is_active = bool(current.data[0].get("is_active")) if current.data else True
        admin.table("platform_api_keys").update({"is_active": not is_active}).eq("id", key_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# STATS GLOBALES COURS
# ============================================================
@router.get("/stats")
async def admin_courses_stats(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        paths = admin.table("paths").select("id").execute()
        chapters = admin.table("course_chapters").select("id").execute()
        lessons = admin.table("course_lessons").select("id").execute()
        blocks = admin.table("lesson_content_blocks").select("id").execute()
        exercises = admin.table("lesson_exercises").select("id").execute()
        unlocks = admin.table("path_unlocks").select("id").execute()
        progress = admin.table("lesson_progress").select("id").execute()

        return {
            "success": True,
            "stats": {
                "paths": len(paths.data or []),
                "chapters": len(chapters.data or []),
                "lessons": len(lessons.data or []),
                "blocks": len(blocks.data or []),
                "exercises": len(exercises.data or []),
                "unlocks": len(unlocks.data or []),
                "completed_lessons": len(progress.data or []),
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))