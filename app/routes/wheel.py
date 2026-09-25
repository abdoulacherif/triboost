from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


@router.get("/config")
async def wheel_config():
    """Renvoie la config des segments de la roue."""
    try:
        admin = get_supabase_admin()
        result = admin.table("wheel_config")\
            .select("*")\
            .eq("is_active", True)\
            .order("sort_order")\
            .execute()

        return {"success": True, "config": result.data or []}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status")
async def wheel_status(request: Request):
    """Retourne si l'utilisateur peut tourner (gratuit dispo ou non)."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()

        # Dernier tour gratuit
        last = admin.table("wheel_spins")\
            .select("created_at")\
            .eq("user_id", user.user.id)\
            .eq("spin_type", "free")\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()

        can_spin_free = True
        next_free_at = None
        if last.data and len(last.data) > 0:
            from datetime import datetime, timedelta, timezone
            last_date = datetime.fromisoformat(last.data[0]["created_at"].replace("Z", "+00:00"))
            next_date = last_date + timedelta(days=7)
            next_free_at = next_date.isoformat()
            can_spin_free = datetime.now(timezone.utc) >= next_date

        # Historique
        history = admin.table("wheel_spins")\
            .select("*")\
            .eq("user_id", user.user.id)\
            .order("created_at", desc=True)\
            .limit(20)\
            .execute()

        return {
            "success": True,
            "can_spin_free": can_spin_free,
            "next_free_at": next_free_at,
            "history": history.data or [],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/spin")
async def spin(request: Request):
    """Fait tourner la roue."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        body = await request.json()
        spin_type = body.get("spin_type", "free")

        if spin_type not in ("free", "paid"):
            raise HTTPException(status_code=400, detail="Type invalide")

        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.rpc("spin_wheel", {
            "p_user_id": user.user.id,
            "p_spin_type": spin_type,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))