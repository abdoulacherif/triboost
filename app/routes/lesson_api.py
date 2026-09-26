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

        # Marquer la session comme terminée (sans vérif de temps)
        try:
            admin.table("lesson_sessions").update({
                "is_finished": True,
                "completed_at": "now()",
            }).eq("id", session_id).eq("user_id", user_id).execute()
        except Exception:
            pass

        # Corriger les exercices
        lesson = admin.table("course_lessons").select("*").eq("id", lesson_id).execute()
        if not lesson.data:
            raise HTTPException(status_code=404, detail="Leçon introuvable")
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

        # Appliquer les gains (via la fonction existante)
        result = admin.rpc("submit_lesson_answers", {
            "p_user_id": user_id,
            "p_lesson_id": lesson_id,
            "p_answers": answers,
        }).execute()

        # Débloquer la prochaine leçon dans 24h
        try:
            unlock = admin.table("path_unlocks").select("id").eq("user_id", user_id).execute()
            if unlock.data:
                for u in unlock.data:
                    admin.table("path_unlocks").update({
                        "next_lesson_available_at": "now() + interval '24 hours'"
                    }).eq("id", u["id"]).execute()
        except Exception:
            pass

        return {
            "success": True,
            "result": result.data if result.data else {},
            "score": {"earned": earned_points, "total": total_points}
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))