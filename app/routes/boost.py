from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# MES FRANCHISES
# ============================================================
@router.get("/franchises/me")
async def my_franchises(request: Request):
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
        result = admin.table("franchises").select("*").eq("user_id", user_response.user.id).order("created_at", desc=True).execute()

        return {"success": True, "franchises": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# LISTER LES ZONES DISPONIBLES
# ============================================================
@router.get("/franchises/zones")
async def available_zones(city: str | None = None):
    try:
        admin = get_supabase_admin()
        query = admin.table("franchises").select("city, quartier").eq("is_active", True)
        if city:
            query = query.eq("city", city)
        taken = query.execute()

        taken_zones = []
        for z in (taken.data or []):
            taken_zones.append(f"{z['city']}|{z.get('quartier', '')}")

        return {"success": True, "taken_zones": taken_zones}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# ACHETER UNE FRANCHISE
# ============================================================
@router.post("/franchises/buy")
async def buy_franchise(request: Request):
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
        city = (body.get("city") or "").strip()
        quartier = (body.get("quartier") or "").strip()

        if not city:
            raise HTTPException(status_code=400, detail="Ville obligatoire")

        admin = get_supabase_admin()

        # Vérifier activation
        profile = admin.table("profiles").select("is_activated").eq("id", user_id).execute()
        raw = profile.data[0].get("is_activated") if profile.data else False
        is_activated = raw is True or raw == "true" or raw == 1 or raw == "1"
        if not is_activated:
            raise HTTPException(status_code=403, detail="Compte non activé")

        result = admin.rpc("buy_franchise", {
            "p_user_id": user_id,
            "p_city": city,
            "p_quartier": quartier,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# STATS FRANCHISE
# ============================================================
@router.get("/franchises/stats")
async def franchise_stats(request: Request):
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
        result = admin.table("franchises").select("total_earned, city, quartier, is_active").eq("user_id", user_response.user.id).execute()

        total = sum(float(f.get("total_earned", 0)) for f in (result.data or []))

        return {
            "success": True,
            "total_earned": total,
            "franchises_count": len(result.data or []),
            "franchises": result.data or [],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))