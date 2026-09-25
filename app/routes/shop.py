from fastapi import APIRouter, HTTPException, Request

from app.core.config import settings
from app.core.supabase_client import get_supabase, get_supabase_admin
from app.integrations.leekpay import create_checkout

router = APIRouter()


# ============================================================
# LISTER LES PRODUITS
# ============================================================
@router.get("/products")
async def list_products():
    try:
        admin = get_supabase_admin()
        result = admin.table("shop_products").select(
            "id, title, description, price, commission, image_url, category, delivery_type"
        ).eq("is_active", True).order("created_at", desc=True).limit(100).execute()
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
# PRODUIT PUBLIC VIA CODE
# ============================================================
@router.get("/p/{code}")
async def get_public_product(code: str):
    try:
        admin = get_supabase_admin()
        aff = admin.table("shop_affiliations").select(
            "*, shop_products(id, title, description, image_url, category, delivery_type), profiles:user_id(full_name)"
        ).eq("affiliate_code", code).eq("is_active", True).execute()

        if not aff.data or len(aff.data) == 0:
            raise HTTPException(status_code=404, detail="Lien introuvable")

        item = aff.data[0]
        product = item.get("shop_products") or {}
        seller = item.get("profiles") or {}

        return {
            "success": True,
            "affiliate": {"code": item["affiliate_code"], "custom_price": item["custom_price"]},
            "product": {
                "id": product.get("id"),
                "title": product.get("title"),
                "description": product.get("description"),
                "image_url": product.get("image_url"),
                "category": product.get("category"),
                "delivery_type": product.get("delivery_type", "virtual"),
            },
            "seller": {"full_name": seller.get("full_name", "Vendeur")},
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# PAYER AVEC LE WALLET (livraison instantanée)
# ============================================================
@router.post("/order-with-wallet")
async def order_with_wallet(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        body = await request.json()
        code = (body.get("affiliate_code") or "").strip()
        quantity = int(body.get("quantity", 1))

        if not code:
            raise HTTPException(status_code=400, detail="Lien invalide")
        if quantity < 1:
            quantity = 1

        admin = get_supabase_admin()
        result = admin.rpc("pay_shop_order_with_wallet", {
            "p_buyer_id": user.user.id,
            "p_affiliate_code": code,
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
# PAYER AVEC LEEKPAY (livraison après confirmation)
# ============================================================
@router.post("/order-with-leekpay")
async def order_with_leekpay(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        body = await request.json()
        code = (body.get("affiliate_code") or "").strip()
        quantity = int(body.get("quantity", 1))
        phone = (body.get("phone") or "").strip()

        if not code or not phone:
            raise HTTPException(status_code=400, detail="Champs obligatoires")

        admin = get_supabase_admin()

        # Récupérer le prix
        aff = admin.table("shop_affiliations").select("custom_price, shop_products(title)").eq("affiliate_code", code).eq("is_active", True).execute()
        if not aff.data or len(aff.data) == 0:
            raise HTTPException(status_code=404, detail="Lien invalide")

        custom_price = float(aff.data[0]["custom_price"])
        product_title = aff.data[0].get("shop_products", {}).get("title", "Produit")
        total = int(custom_price * quantity)

        # Créer la commande en attente
        create_result = admin.rpc("create_pending_shop_order", {
            "p_buyer_id": user.user.id,
            "p_affiliate_code": code,
            "p_quantity": quantity,
            "p_buyer_name": "",
            "p_buyer_phone": phone,
            "p_checkout_id": "",
        }).execute()

        if not create_result.data or not create_result.data.get("success"):
            raise HTTPException(status_code=400, detail=create_result.data.get("message", "Erreur"))

        order_id = create_result.data["order_id"]

        # Créer checkout LeekPay
        user_email = user.user.email
        checkout = await create_checkout(
            amount=total,
            currency="XOF",
            description=f"Achat : {product_title}",
            return_url=f"{settings.BASE_URL}/shop/success?order_id={order_id}",
            cancel_url=f"{settings.BASE_URL}/shop/p/{code}",
            customer_email=user_email,
            customer_phone=phone,
            metadata={
                "user_id": user.user.id,
                "order_id": str(order_id),
                "type": "shop_order",
                "code": code,
            },
        )

        # Mettre à jour le checkout_id
        admin.table("shop_orders").update({"notes": checkout.get("id")}).eq("id", order_id).execute()

        return {
            "success": True,
            "payment_url": checkout.get("payment_url"),
            "checkout_id": checkout.get("id"),
            "order_id": order_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# VÉRIFIER STATUT COMMANDE
# ============================================================
@router.get("/order/{order_id}")
async def get_order_status(order_id: str, request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.table("shop_orders").select("*").eq("id", order_id).execute()

        if not result.data or len(result.data) == 0:
            raise HTTPException(status_code=404, detail="Commande introuvable")

        order = result.data[0]

        return {
            "success": True,
            "order": {
                "id": order["id"],
                "status": order["status"],
                "total_paid": order["total_paid"],
                "content_url": order.get("delivery_content_url") or "",
                "content_text": order.get("delivery_content_text") or "",
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MES VENTES (affilié)
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


# ============================================================
# MES ACHATS (client)
# ============================================================
@router.get("/my-purchases")
async def my_purchases(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.table("shop_purchases").select(
            "*, shop_products(title, image_url), shop_orders(delivery_content_url, delivery_content_text, total_paid, status, created_at)"
        ).eq("buyer_user_id", user.user.id).order("created_at", desc=True).execute()

        return {"success": True, "purchases": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))