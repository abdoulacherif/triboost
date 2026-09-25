from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


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
        raise HTTPException(status_code=403, detail="Non autorisé")
    return user.user.id


# ============================================================
# PRODUITS
# ============================================================
@router.get("/products")
async def admin_list_products(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.table("shop_products").select("*").order("created_at", desc=True).limit(100).execute()
        return {"success": True, "products": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/products/create")
async def admin_create_product(request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        title = (body.get("title") or "").strip()
        price = float(body.get("price", 0))
        commission = float(body.get("commission", 0))

        if not title or price <= 0:
            raise HTTPException(status_code=400, detail="Titre et prix obligatoires")

        if commission >= price:
            raise HTTPException(status_code=400, detail="La commission doit être inférieure au prix")

        result = admin.table("shop_products").insert({
            "title": title,
            "description": body.get("description", ""),
            "price": price,
            "commission": commission,
            "image_url": body.get("image_url", ""),
            "category": body.get("category", "autre"),
            "is_active": True,
        }).execute()

        return {"success": True, "product": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/products/{product_id}/update")
async def admin_update_product(product_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        update_data = {}
        for f in ["title", "description", "image_url", "category"]:
            if f in body:
                update_data[f] = body[f]
        if "price" in body:
            update_data["price"] = float(body["price"])
        if "commission" in body:
            update_data["commission"] = float(body["commission"])
        if "is_active" in body:
            update_data["is_active"] = bool(body["is_active"])

        if update_data:
            admin.table("shop_products").update(update_data).eq("id", product_id).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/products/{product_id}")
async def admin_delete_product(product_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("shop_products").delete().eq("id", product_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# COMMANDES
# ============================================================
@router.get("/orders")
async def admin_list_orders(request: Request, status: str = "all"):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        q = admin.table("shop_orders").select(
            "*, shop_products(title, image_url)"
        ).order("created_at", desc=True).limit(100)

        if status and status != "all":
            q = q.eq("status", status)

        result = q.execute()
        items = result.data or []

        # Ajouter noms des vendeurs
        if items:
            aff_ids = list(set(i["affiliate_id"] for i in items))
            affs = admin.table("shop_affiliations").select("id, user_id, affiliate_code").in_("id", aff_ids).execute()
            aff_map = {a["id"]: a for a in (affs.data or [])}

            user_ids = list(set(a["user_id"] for a in aff_map.values()))
            users = admin.table("profiles").select("id, full_name").in_("id", user_ids).execute()
            user_map = {u["id"]: u.get("full_name", "") for u in (users.data or [])}

            for i in items:
                aff = aff_map.get(i["affiliate_id"])
                if aff:
                    i["seller_name"] = user_map.get(aff["user_id"], "Vendeur")
                    i["affiliate_code"] = aff.get("affiliate_code", "")

        return {"success": True, "orders": items}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/orders/{order_id}/complete")
async def admin_complete_order(order_id: str, request: Request):
    try:
        admin_id = await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.rpc("admin_complete_shop_order", {
            "p_admin_id": admin_id,
            "p_order_id": order_id,
        }).execute()
        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/orders/{order_id}")
async def admin_delete_order(order_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("shop_orders").delete().eq("id", order_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# AFFILIATIONS
# ============================================================
@router.get("/affiliations")
async def admin_list_affiliations(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()

        result = admin.table("shop_affiliations").select(
            "*, shop_products(title, price, commission)"
        ).order("created_at", desc=True).limit(100).execute()

        items = result.data or []

        if items:
            user_ids = list(set(i["user_id"] for i in items))
            users = admin.table("profiles").select("id, full_name").in_("id", user_ids).execute()
            user_map = {u["id"]: u.get("full_name", "") for u in (users.data or [])}
            for i in items:
                i["user_name"] = user_map.get(i["user_id"], "")

        return {"success": True, "affiliations": items}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/affiliations/{aff_id}")
async def admin_delete_affiliation(aff_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("shop_affiliations").delete().eq("id", aff_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))