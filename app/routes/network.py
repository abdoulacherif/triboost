from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase

router = APIRouter()


@router.get("/stats")
async def network_stats(request: Request):
    """Retourne les statistiques du réseau (comptes + gains par niveau)."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        supabase = get_supabase()

        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        result = supabase.rpc(
            "get_network_stats",
            {"p_user_id": user_response.user.id}
        ).execute()

        return {"success": True, "stats": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/downline")
async def network_downline(request: Request):
    """Retourne les filleuls organisés par niveau."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        supabase = get_supabase()

        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        result = supabase.rpc(
            "get_network",
            {"p_user_id": user_response.user.id}
        ).execute()

        # Organiser par niveau
        downline = {"n1": [], "n2": [], "n3": []}
        for item in (result.data or []):
            level = item.get("level")
            if level == 1:
                downline["n1"].append(item)
            elif level == 2:
                downline["n2"].append(item)
            elif level == 3:
                downline["n3"].append(item)

        return {"success": True, "downline": downline}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))