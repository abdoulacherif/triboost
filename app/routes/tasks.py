from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# LISTER LES TÂCHES DISPONIBLES
# ============================================================
@router.get("/")
async def list_tasks(request: Request):
    """Liste toutes les tâches actives + statut de l'utilisateur."""
    try:
        admin = get_supabase_admin()

        # Récupérer les tâches
        result = (
            admin.table("tasks")
            .select("*")
            .eq("is_active", True)
            .order("sort_order", desc=False)
            .order("created_at", desc=True)
            .execute()
        )
        tasks = result.data or []

        # Si connecté, récupérer les soumissions de l'utilisateur
        user_submissions = {}
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                supabase_anon = get_supabase()
                user = supabase_anon.auth.get_user(token)
                if user.user:
                    subs = (
                        admin.table("task_submissions")
                        .select("task_id, status, reward, created_at, validated_at, admin_note")
                        .eq("user_id", user.user.id)
                        .execute()
                    )
                    for s in (subs.data or []):
                        user_submissions[s["task_id"]] = s
            except Exception:
                pass

        # Fusionner
        for t in tasks:
            sub = user_submissions.get(t["id"])
            t["user_status"] = sub["status"] if sub else None
            t["user_submission"] = sub if sub else None

        return {"success": True, "tasks": tasks, "count": len(tasks)}

    except Exception as e:
        print(f"[TASKS] Erreur list: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SOUMETTRE UNE PREUVE
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

        body = await request.json()
        network = (body.get("network") or "").strip()
        proof_url = (body.get("proof_url") or "").strip()
        comment = (body.get("comment") or "").strip()

        if not network:
            raise HTTPException(status_code=400, detail="Réseau obligatoire")
        if not proof_url:
            raise HTTPException(status_code=400, detail="Lien de preuve obligatoire")

        admin = get_supabase_admin()

        # Vérifier que la tâche existe
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

        # Vérifier le quota
        if task["max_completions"] > 0 and task["completed_count"] >= task["max_completions"]:
            raise HTTPException(status_code=400, detail="Cette tâche est complète")

        # Vérifier si déjà soumis
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
            # Si "rejected", on permet de resoumettre (update)

        # Insérer ou mettre à jour
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


# ============================================================
# MES SOUMISSIONS
# ============================================================
@router.get("/my-submissions")
async def my_submissions(request: Request):
    """Retourne les soumissions de l'utilisateur."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = (
            admin.table("task_submissions")
            .select("id, task_id, network, proof_url, status, reward, admin_note, created_at, validated_at, tasks(title, icon)")
            .eq("user_id", user_response.user.id)
            .order("created_at", desc=True)
            .execute()
        )

        return {"success": True, "submissions": result.data or []}

    except HTTPException:
        raise
    except Exception as e:
        print(f"[TASKS] Erreur my-submissions: {e}")
        raise HTTPException(status_code=400, detail=str(e))