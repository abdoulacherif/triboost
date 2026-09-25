from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# LISTER LES PRODUITS (public)
# ============================================================
@router.get("/products")
async def list_products():
    try:
        admin = get_supabase_admin()
        result = admin.table("shop_products").select("*").eq("is_active", True).order("created_at", desc=True).limit(100).execute()
        return {"success": True, "products": result.data or []}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MES AFFILIATIONS
# ============================================================
@router.get("/my-affiliations")
async def my_affiliations(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.table("shop_affiliations").select(
            "*, shop_products(title, image_url, price, commission)"
        ).eq("user_id", user.user.id).order("created_at", desc=True).execute()

        return {"success": True, "affiliations": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# AFFILIER UN PRODUIT
# ============================================================
@router.post("/affiliate/{product_id}")
async def affiliate(product_id: str, request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        body = await request.json()
        custom_price = float(body.get("custom_price", 0))

        if custom_price <= 0:
            raise HTTPException(status_code=400, detail="Prix invalide")

        admin = get_supabase_admin()

        # Vérifier activation
        profile = admin.table("profiles").select("is_activated").eq("id", user.user.id).execute()
        raw = profile.data[0].get("is_activated") if profile.data else False
        is_activated = raw is True or raw == "true" or raw == 1 or raw == "1"
        if not is_activated:
            raise HTTPException(status_code=403, detail="Compte non activé")

        result = admin.rpc("affiliate_product", {
            "p_user_id": user.user.id,
            "p_product_id": product_id,
            "p_custom_price": custom_price,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SUPPRIMER UNE AFFILIATION
# ============================================================
@router.delete("/affiliate/{affiliation_id}")
async def delete_affiliation(affiliation_id: str, request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        admin.table("shop_affiliations").delete().eq("id", affiliation_id).eq("user_id", user.user.id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# PRODUIT PUBLIC VIA CODE AFFILIÉ
# ============================================================
@router.get("/p/{code}")
async def get_public_product(code: str):
    try:
        admin = get_supabase_admin()

        aff = admin.table("shop_affiliations").select(
            "*, shop_products(*), profiles:user_id(full_name)"
        ).eq("affiliate_code", code).eq("is_active", True).execute()

        if not aff.data or len(aff.data) == 0:
            raise HTTPException(status_code=404, detail="Lien introuvable")

        item = aff.data[0]
        product = item.get("shop_products") or {}
        seller = item.get("profiles") or {}

        return {
            "success": True,
            "affiliate": {
                "code": item["affiliate_code"],
                "custom_price": item["custom_price"],
            },
            "product": {
                "id": product.get("id"),
                "title": product.get("title"),
                "description": product.get("description"),
                "image_url": product.get("image_url"),
                "category": product.get("category"),
            },
            "seller": {
                "full_name": seller.get("full_name", "Vendeur"),
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# CRÉER UNE COMMANDE (public, pas besoin de compte)
# ============================================================
@router.post("/order")
async def create_order(request: Request):
    try:
        body = await request.json()
        code = (body.get("affiliate_code") or "").strip()
        name = (body.get("buyer_name") or "").strip()
        phone = (body.get("buyer_phone") or "").strip()
        email = (body.get("buyer_email") or "").strip()
        address = (body.get("buyer_address") or "").strip()
        quantity = int(body.get("quantity", 1))

        if not code or not name or not phone:
            raise HTTPException(status_code=400, detail="Nom et téléphone obligatoires")
        if quantity < 1:
            quantity = 1

        admin = get_supabase_admin()
        result = admin.rpc("create_shop_order", {
            "p_affiliate_code": code,
            "p_buyer_name": name,
            "p_buyer_phone": phone,
            "p_buyer_email": email,
            "p_buyer_address": address,
            "p_quantity": quantity,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MES VENTES
# ============================================================
@router.get("/my-sales")
async def my_sales(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()

        # Mes affiliations
        affs = admin.table("shop_affiliations").select("id").eq("user_id", user.user.id).execute()
        aff_ids = [a["id"] for a in (affs.data or [])]

        if not aff_ids:
            return {"success": True, "sales": []}

        sales = admin.table("shop_orders").select(
            "*, shop_products(title, image_url)"
        ).in_("affiliate_id", aff_ids).order("created_at", desc=True).limit(100).execute()

        return {"success": True, "sales": sales.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))