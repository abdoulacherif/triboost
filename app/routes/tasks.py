# ============================================================
# SOUMETTRE UNE PREUVE (⚠️ compte activé requis)
# ============================================================
@router.post("/{task_id}/submit")
async def submit_task(task_id: str, request: Request):
    """Soumet une preuve pour valider une tâche."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")

        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user_response.user.id
        admin = get_supabase_admin()

        # ⚠️ VÉRIFIER QUE LE COMPTE EST ACTIVÉ
        profile_check = (
            admin.table("profiles")
            .select("is_activated")
            .eq("id", user_id)
            .execute()
        )

        is_activated = False
        if profile_check.data and len(profile_check.data) > 0:
            raw = profile_check.data[0].get("is_activated")
            is_activated = raw is True or raw == "true" or raw == 1 or raw == "1"

        if not is_activated:
            raise HTTPException(
                status_code=403,
                detail="Compte non activé. Activez pour 3 600 FCFA pour accomplir des tâches."
            )

        body = await request.json()
        network = (body.get("network") or "").strip()
        proof_url = (body.get("proof_url") or "").strip()
        comment = (body.get("comment") or "").strip()

        if not network:
            raise HTTPException(status_code=400, detail="Réseau obligatoire")
        if not proof_url:
            raise HTTPException(status_code=400, detail="Lien de preuve obligatoire")

        task_result = (
            admin.table("tasks")
            .select("id, reward, is_active, max_completions, completed_count")
            .eq("id", task_id)
            .eq("is_active", True)
            .execute()
        )

        if not task_result.data or len(task_result.data) == 0:
            raise HTTPException(status_code=404, detail="Tâche introuvable ou inactive")

        task = task_result.data[0]

        if task["max_completions"] > 0 and task["completed_count"] >= task["max_completions"]:
            raise HTTPException(status_code=400, detail="Cette tâche est complète")

        existing = (
            admin.table("task_submissions")
            .select("id, status")
            .eq("user_id", user_id)
            .eq("task_id", task_id)
            .execute()
        )

        if existing.data and len(existing.data) > 0:
            status = existing.data[0]["status"]
            if status == "pending":
                raise HTTPException(status_code=400, detail="Tu as déjà une soumission en attente")
            if status == "approved":
                raise HTTPException(status_code=400, detail="Tu as déjà validé cette tâche")

        if existing.data and len(existing.data) > 0:
            admin.table("task_submissions").update({
                "network": network,
                "proof_url": proof_url,
                "comment": comment,
                "status": "pending",
                "admin_note": "",
            }).eq("id", existing.data[0]["id"]).execute()
        else:
            admin.table("task_submissions").insert({
                "task_id": task_id,
                "user_id": user_id,
                "network": network,
                "proof_url": proof_url,
                "comment": comment,
                "reward": task["reward"],
                "status": "pending",
            }).execute()

        return {
            "success": True,
            "message": "Soumission envoyée ! Vérification sous 24-48h.",
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[TASKS] Erreur submit: {e}")
        raise HTTPException(status_code=400, detail=str(e))