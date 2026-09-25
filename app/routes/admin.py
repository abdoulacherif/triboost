from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# VÉRIFICATION ADMIN
# ============================================================
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
        raise HTTPException(status_code=403, detail="Accès réservé aux admins")

    return user.user.id


# ============================================================
# STATS GLOBALES
# ============================================================
@router.get("/stats")
async def admin_stats(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        users = admin.table("profiles").select("id, is_activated, wallet_balance").execute()
        users_list = users.data or []

        tasks_pending = admin.table("task_submissions").select("id").eq("status", "pending").execute()
        withdrawals_pending = admin.table("withdrawals").select("id").eq("status", "pending").execute()
        recharges_pending = admin.table("recharges").select("id").eq("status", "pending").execute()

        return {
            "success": True,
            "stats": {
                "total_users": len(users_list),
                "activated_users": sum(1 for u in users_list if u.get("is_activated")),
                "total_wallets": sum(float(u.get("wallet_balance", 0) or 0) for u in users_list),
                "tasks_pending": len(tasks_pending.data or []),
                "withdrawals_pending": len(withdrawals_pending.data or []),
                "recharges_pending": len(recharges_pending.data or []),
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ADMIN] stats: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# UTILISATEURS
# ============================================================
@router.get("/users")
async def list_users(request: Request, search: str = ""):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        result = admin.table("profiles").select(
            "id, full_name, phone, country, referral_code, referred_by, is_activated, is_admin, is_banned, wallet_balance, total_earned, created_at"
        ).order("created_at", desc=True).limit(200).execute()

        users = result.data or []

        # Récupérer les emails via auth admin
        try:
            auth_users = admin.auth.admin.list_users()
            email_map = {}
            if hasattr(auth_users, "users"):
                for u in auth_users.users:
                    email_map[str(u.id)] = u.email
            elif isinstance(auth_users, list):
                for u in auth_users:
                    email_map[str(u.id)] = u.email
            for u in users:
                u["email"] = email_map.get(u["id"], "")
        except Exception as e:
            print(f"[ADMIN] emails: {e}")

        if search:
            s = search.lower()
            users = [u for u in users if
                     s in (u.get("full_name", "") or "").lower()
                     or s in (u.get("email", "") or "").lower()
                     or s in (u.get("phone", "") or "").lower()
                     or s in (u.get("referral_code", "") or "").lower()]

        return {"success": True, "users": users}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ADMIN] users: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/users/{user_id}/balance")
async def update_balance(user_id: str, request: Request):
    try:
        admin_id = await _check_admin(request)
        body = await request.json()
        new_balance = float(body.get("balance", 0))

        admin = get_supabase_admin()
        current = admin.table("profiles").select("wallet_balance").eq("id", user_id).execute()
        old_balance = float(current.data[0].get("wallet_balance", 0) or 0) if current.data else 0

        admin.rpc("admin_update_balance", {
            "p_admin_id": admin_id,
            "p_user_id": user_id,
            "p_amount": old_balance,
            "p_new_balance": new_balance,
        }).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/users/{user_id}/toggle-activation")
async def toggle_activation(user_id: str, request: Request):
    try:
        admin_id = await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.rpc("admin_toggle_activation", {
            "p_admin_id": admin_id,
            "p_user_id": user_id,
        }).execute()
        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# PARRAINAGE
# ============================================================
@router.get("/referrals")
async def list_referrals(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        users = admin.table("profiles").select(
            "id, full_name, referral_code, referred_by, is_activated, created_at"
        ).execute()
        users_list = users.data or []
        users_map = {u["id"]: u for u in users_list}

        tree = []
        for u in users_list:
            referrer = users_map.get(u.get("referred_by")) if u.get("referred_by") else None
            tree.append({"user": u, "referrer": referrer})

        for u in users_list:
            u["filleuls_directs"] = sum(1 for x in users_list if x.get("referred_by") == u["id"])

        return {"success": True, "referrals": tree}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SOUMISSIONS DE TÂCHES (à valider)
# ============================================================
@router.get("/tasks")
async def list_tasks_admin(request: Request, status: str = "pending"):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        q = admin.table("task_submissions").select(
            "id, user_id, task_id, network, proof_url, comment, status, reward, admin_note, created_at, tasks(title, icon)"
        ).order("created_at", desc=True).limit(100)

        if status and status != "all":
            q = q.eq("status", status)

        result = q.execute()
        items = result.data or []

        if items:
            user_ids = list(set(i["user_id"] for i in items))
            users = admin.table("profiles").select("id, full_name").in_("id", user_ids).execute()
            users_map = {u["id"]: u.get("full_name", "") for u in (users.data or [])}
            for i in items:
                i["user_name"] = users_map.get(i["user_id"], "")

        return {"success": True, "tasks": items}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tasks/{submission_id}/review")
async def review_task(submission_id: str, request: Request):
    try:
        admin_id = await _check_admin(request)
        body = await request.json()
        status = body.get("status")
        note = body.get("note", "")

        admin = get_supabase_admin()
        result = admin.rpc("admin_review_task", {
            "p_admin_id": admin_id,
            "p_submission_id": submission_id,
            "p_status": status,
            "p_note": note,
        }).execute()

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/submissions/{submission_id}")
async def admin_delete_submission(submission_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("task_submissions").delete().eq("id", submission_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# GESTION DES TÂCHES (le catalogue)
# ============================================================
@router.get("/tasks-all")
async def admin_list_all_tasks(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.table("tasks").select("*").order("sort_order").order("created_at", desc=True).execute()
        return {"success": True, "tasks": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tasks/create")
async def admin_create_task(request: Request):
    try:
        await _check_admin(request)
        body = await request.json()

        title = (body.get("title") or "").strip()
        description = (body.get("description") or "").strip()
        instructions = (body.get("instructions") or "").strip()
        reward = float(body.get("reward", 0))
        icon = body.get("icon", "🎯") or "🎯"
        network_hint = body.get("network_hint", "") or ""

        if not title or reward <= 0:
            raise HTTPException(status_code=400, detail="Titre et récompense obligatoires")

        admin = get_supabase_admin()
        result = admin.table("tasks").insert({
            "title": title,
            "description": description,
            "instructions": instructions,
            "reward": reward,
            "icon": icon,
            "network_hint": network_hint,
            "is_active": True,
        }).execute()

        return {"success": True, "task": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tasks/{task_id}/update")
async def admin_update_task(task_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()

        update_data = {}
        for field in ["title", "description", "instructions", "icon", "network_hint"]:
            if field in body:
                update_data[field] = body[field]
        if "reward" in body:
            update_data["reward"] = float(body["reward"])
        if "is_active" in body:
            update_data["is_active"] = bool(body["is_active"])

        if not update_data:
            raise HTTPException(status_code=400, detail="Rien à modifier")

        admin = get_supabase_admin()
        admin.table("tasks").update(update_data).eq("id", task_id).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/tasks/{task_id}")
async def admin_delete_task(task_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("tasks").delete().eq("id", task_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# RETRAITS
# ============================================================
@router.get("/withdrawals")
async def list_withdrawals_admin(request: Request, status: str = "pending"):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        q = admin.table("withdrawals").select("*").order("created_at", desc=True).limit(100)
        if status and status != "all":
            q = q.eq("status", status)

        result = q.execute()
        items = result.data or []

        if items:
            user_ids = list(set(i["user_id"] for i in items))
            users = admin.table("profiles").select("id, full_name").in_("id", user_ids).execute()
            users_map = {u["id"]: u.get("full_name", "") for u in (users.data or [])}
            for i in items:
                i["user_name"] = users_map.get(i["user_id"], "")

        return {"success": True, "withdrawals": items}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/withdrawals/{withdrawal_id}/review")
async def review_withdrawal(withdrawal_id: str, request: Request):
    try:
        admin_id = await _check_admin(request)
        body = await request.json()
        status = body.get("status")
        note = body.get("note", "")

        admin = get_supabase_admin()
        result = admin.rpc("admin_review_withdrawal", {
            "p_admin_id": admin_id,
            "p_withdrawal_id": withdrawal_id,
            "p_status": status,
            "p_note": note,
        }).execute()

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/withdrawals/{withdrawal_id}")
async def admin_delete_withdrawal(withdrawal_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("withdrawals").delete().eq("id", withdrawal_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# RECHARGES
# ============================================================
@router.get("/recharges")
async def list_recharges_admin(request: Request, status: str = "pending"):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        q = admin.table("recharges").select("*").order("created_at", desc=True).limit(100)
        if status and status != "all":
            q = q.eq("status", status)

        result = q.execute()
        items = result.data or []

        if items:
            user_ids = list(set(i["user_id"] for i in items))
            users = admin.table("profiles").select("id, full_name").in_("id", user_ids).execute()
            users_map = {u["id"]: u.get("full_name", "") for u in (users.data or [])}
            for i in items:
                i["user_name"] = users_map.get(i["user_id"], "")

        return {"success": True, "recharges": items}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/recharges/{recharge_id}/confirm")
async def confirm_recharge_admin(recharge_id: str, request: Request):
    try:
        admin_id = await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.rpc("admin_confirm_recharge", {
            "p_admin_id": admin_id,
            "p_recharge_id": recharge_id,
        }).execute()
        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/recharges/{recharge_id}")
async def admin_delete_recharge(recharge_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("recharges").delete().eq("id", recharge_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))