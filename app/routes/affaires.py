from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# SERVICES DIGITAUX — LISTER
# ============================================================
@router.get("/services")
async def list_services(
    category: str | None = None,
    search: str | None = None,
):
    try:
        admin = get_supabase_admin()
        query = (
            admin.table("digital_services")
            .select("id, title, description, category, price, delivery_time, portfolio_url, cover_url, rating, total_orders, created_at, user_id")
            .eq("is_active", True)
            .order("created_at", desc=True)
            .limit(100)
        )
        if category and category != "tous":
            query = query.eq("category", category)

        result = query.execute()
        items = result.data or []

        if search:
            s = search.lower()
            items = [
                i for i in items
                if s in (i.get("title", "") or "").lower()
                or s in (i.get("description", "") or "").lower()
            ]

        return {"success": True, "services": items, "count": len(items)}
    except Exception as e:
        print(f"[AFFAIRES] Erreur list services: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SERVICES DIGITAUX — CRÉER (compte activé requis)
# ============================================================
@router.post("/services")
async def create_service(request: Request):
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

        # Vérifier activation
        profile = admin.table("profiles").select("is_activated").eq("id", user_id).execute()
        if not profile.data or len(profile.data) == 0:
            raise HTTPException(status_code=403, detail="Profil introuvable")

        raw = profile.data[0].get("is_activated")
        is_activated = raw is True or raw == "true" or raw == 1 or raw == "1"
        if not is_activated:
            raise HTTPException(status_code=403, detail="Compte non activé")

        body = await request.json()
        title = (body.get("title") or "").strip()
        description = (body.get("description") or "").strip()
        category = (body.get("category") or "autre").strip()
        price = float(body.get("price") or 0)
        delivery_time = (body.get("delivery_time") or "3 jours").strip()
        portfolio_url = (body.get("portfolio_url") or "").strip()

        if not title or price <= 0:
            raise HTTPException(status_code=400, detail="Titre et prix valides obligatoires")

        insert = admin.table("digital_services").insert({
            "user_id": user_id,
            "title": title,
            "description": description,
            "category": category,
            "price": price,
            "delivery_time": delivery_time,
            "portfolio_url": portfolio_url,
        }).execute()

        if not insert.data or len(insert.data) == 0:
            raise HTTPException(status_code=400, detail="Erreur de création")

        return {"success": True, "service": insert.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[AFFAIRES] Erreur create service: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SERVICES DIGITAUX — SUPPRIMER
# ============================================================
@router.delete("/services/{service_id}")
async def delete_service(service_id: str, request: Request):
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
        admin.table("digital_services").delete().eq("id", service_id).eq("user_id", user_response.user.id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# DEVENIR REVENDEUR
# ============================================================
@router.post("/reseller/become")
async def become_reseller(request: Request):
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

        # Vérifier activation
        profile = admin.table("profiles").select("is_activated").eq("id", user_id).execute()
        raw = profile.data[0].get("is_activated") if profile.data else False
        is_activated = raw is True or raw == "true" or raw == 1 or raw == "1"
        if not is_activated:
            raise HTTPException(status_code=403, detail="Compte non activé")

        result = admin.rpc("become_reseller", {"p_user_id": user_id}).execute()
        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MON PROFIL REVENDEUR
# ============================================================
@router.get("/reseller/me")
async def my_reseller(request: Request):
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
        result = admin.table("resellers").select("*").eq("user_id", user_response.user.id).execute()

        if not result.data or len(result.data) == 0:
            return {"success": True, "reseller": None}

        return {"success": True, "reseller": result.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MES VENTES REVENDEUR
# ============================================================
@router.get("/reseller/sales")
async def my_sales(request: Request):
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
        reseller = admin.table("resellers").select("id").eq("user_id", user_response.user.id).execute()
        if not reseller.data or len(reseller.data) == 0:
            return {"success": True, "sales": []}

        reseller_id = reseller.data[0]["id"]
        sales = admin.table("reseller_sales")\
            .select("id, formation_id, amount, commission, status, created_at, formations(title)")\
            .eq("reseller_id", reseller_id)\
            .order("created_at", desc=True)\
            .execute()

        return {"success": True, "sales": sales.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))