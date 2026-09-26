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
# QUESTIONS
# ============================================================
@router.post("/questions/create")
async def create_question(request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        if not body.get("lesson_id") or not body.get("question"):
            raise HTTPException(status_code=400, detail="Champs obligatoires")

        result = admin.table("lesson_questions").insert({
            "lesson_id": body["lesson_id"],
            "question": body["question"],
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