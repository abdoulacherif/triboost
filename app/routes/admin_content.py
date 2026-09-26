import base64
import uuid

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
# UPLOAD IMAGE (helper)
# ============================================================
def _upload_image(admin, base64_str: str, folder: str = "covers") -> str:
    """Upload une image base64 vers Supabase Storage, retourne l'URL publique."""
    try:
        header, b64data = base64_str.split(",", 1)
        ext = "jpg"
        if "png" in header:
            ext = "png"
        elif "webp" in header:
            ext = "webp"
        elif "gif" in header:
            ext = "gif"

        img_bytes = base64.b64decode(b64data)
        if len(img_bytes) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image trop lourde (max 5 MB)")

        filename = f"{folder}/{uuid.uuid4().hex}.{ext}"
        admin.storage.from_("formations").upload(
            path=filename,
            file=img_bytes,
            file_options={"content-type": f"image/{ext}"},
        )
        return admin.storage.from_("formations").get_public_url(filename)
    except HTTPException:
        raise
    except Exception as e:
        print(f"[UPLOAD] Erreur: {e}")
        return ""


# ============================================================
# UTILISATEUR — MODIFIER
# ============================================================
@router.post("/user/{user_id}/update")
async def admin_update_user(user_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        update_data = {}
        for field in ["full_name", "phone", "country", "referral_code"]:
            if field in body:
                update_data[field] = body[field]
        if "is_banned" in body:
            update_data["is_banned"] = bool(body["is_banned"])
        if "admin_note" in body:
            update_data["admin_note"] = body["admin_note"]

        if update_data:
            admin.table("profiles").update(update_data).eq("id", user_id).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MARCHÉ
# ============================================================
@router.get("/market")
async def admin_list_market(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.table("marketplace_items").select(
            "id, title, description, price, category, city, whatsapp, image_url, is_active, is_banned, user_id, created_at"
        ).order("created_at", desc=True).limit(50).execute()
        items = result.data or []

        if items:
            uids = list(set(i["user_id"] for i in items))
            users = admin.table("profiles").select("id, full_name").in_("id", uids).execute()
            umap = {u["id"]: u.get("full_name", "") for u in (users.data or [])}
            for i in items:
                i["user_name"] = umap.get(i["user_id"], "")

        return {"success": True, "items": items}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/market/{item_id}")
async def admin_delete_market(item_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("marketplace_items").delete().eq("id", item_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/market/{item_id}/ban")
async def admin_ban_market(item_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()
        admin.table("marketplace_items").update({
            "is_banned": True,
            "is_active": False,
            "ban_reason": body.get("reason", ""),
        }).eq("id", item_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SERVICES
# ============================================================
@router.get("/services")
async def admin_list_services(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.table("digital_services").select(
            "id, title, description, category, price, delivery_time, is_active, is_banned, user_id, created_at"
        ).order("created_at", desc=True).limit(50).execute()
        items = result.data or []

        if items:
            uids = list(set(i["user_id"] for i in items))
            users = admin.table("profiles").select("id, full_name").in_("id", uids).execute()
            umap = {u["id"]: u.get("full_name", "") for u in (users.data or [])}
            for i in items:
                i["user_name"] = umap.get(i["user_id"], "")

        return {"success": True, "items": items}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/services/{service_id}")
async def admin_delete_service(service_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("digital_services").delete().eq("id", service_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/services/{service_id}/ban")
async def admin_ban_service(service_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()
        admin.table("digital_services").update({
            "is_banned": True,
            "is_active": False,
            "ban_reason": body.get("reason", ""),
        }).eq("id", service_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# FRANCHISES
# ============================================================
@router.get("/franchises")
async def admin_list_franchises(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.table("franchises").select(
            "id, city, quartier, price_paid, is_active, total_earned, user_id, created_at"
        ).order("created_at", desc=True).limit(50).execute()
        items = result.data or []

        if items:
            uids = list(set(i["user_id"] for i in items))
            users = admin.table("profiles").select("id, full_name").in_("id", uids).execute()
            umap = {u["id"]: u.get("full_name", "") for u in (users.data or [])}
            for i in items:
                i["user_name"] = umap.get(i["user_id"], "")

        return {"success": True, "items": items}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/franchises/{franchise_id}")
async def admin_delete_franchise(franchise_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("franchises").delete().eq("id", franchise_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/franchises/{franchise_id}/toggle")
async def admin_toggle_franchise(franchise_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        current = admin.table("franchises").select("is_active").eq("id", franchise_id).execute()
        is_active = bool(current.data[0].get("is_active")) if current.data else True
        admin.table("franchises").update({"is_active": not is_active}).eq("id", franchise_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# FORMATIONS
# ============================================================
@router.get("/formations")
async def admin_list_formations(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.table("formations").select(
            "id, title, description, category, cover_url, content_url, content_text, duration, level, price, is_free, is_published, is_banned, views, created_at"
        ).order("created_at", desc=True).limit(50).execute()
        return {"success": True, "items": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/formations/create")
async def admin_create_formation(request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        if not body.get("title"):
            raise HTTPException(status_code=400, detail="Titre obligatoire")

        # Image : upload depuis base64 OU utiliser l'URL fournie
        cover_url = body.get("cover_url", "") or ""
        if body.get("image_base64"):
            uploaded = _upload_image(admin, body["image_base64"], "covers")
            if uploaded:
                cover_url = uploaded

        result = admin.table("formations").insert({
            "title": body.get("title", ""),
            "description": body.get("description", ""),
            "category": body.get("category", "autre"),
            "cover_url": cover_url,
            "content_url": body.get("content_url", ""),
            "content_text": body.get("content_text", ""),
            "duration": body.get("duration", ""),
            "level": body.get("level", "débutant"),
            "price": float(body.get("price", 0)),
            "is_free": bool(body.get("is_free", False)),
            "is_published": bool(body.get("is_published", True)),
            "author": body.get("author", "TriBoost"),
        }).execute()

        return {"success": True, "item": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/formations/{formation_id}/update")
async def admin_update_formation(formation_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        update_data = {}
        for f in ["title", "description", "category", "content_url", "content_text", "duration", "level", "author"]:
            if f in body:
                update_data[f] = body[f]

        # Image : upload si base64, sinon URL fournie
        if body.get("image_base64"):
            uploaded = _upload_image(admin, body["image_base64"], "covers")
            if uploaded:
                update_data["cover_url"] = uploaded
        elif "cover_url" in body:
            update_data["cover_url"] = body["cover_url"]

        if "price" in body:
            update_data["price"] = float(body["price"])
        if "is_free" in body:
            update_data["is_free"] = bool(body["is_free"])
        if "is_published" in body:
            update_data["is_published"] = bool(body["is_published"])
        if "is_banned" in body:
            update_data["is_banned"] = bool(body["is_banned"])

        if update_data:
            admin.table("formations").update(update_data).eq("id", formation_id).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/formations/{formation_id}")
async def admin_delete_formation(formation_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("formations").delete().eq("id", formation_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# PARCOURS
# ============================================================
@router.get("/paths")
async def admin_list_paths(request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        result = admin.table("paths").select(
            "id, title, description, icon, color, reward_per_formation, bonus_final, is_active, created_at"
        ).order("sort_order").limit(50).execute()
        return {"success": True, "items": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/paths/{path_id}/update")
async def admin_update_path(path_id: str, request: Request):
    try:
        await _check_admin(request)
        body = await request.json()
        admin = get_supabase_admin()

        update_data = {}
        for f in ["title", "description", "icon", "color"]:
            if f in body:
                update_data[f] = body[f]
        if "reward_per_formation" in body:
            update_data["reward_per_formation"] = float(body["reward_per_formation"])
        if "bonus_final" in body:
            update_data["bonus_final"] = float(body["bonus_final"])
        if "is_active" in body:
            update_data["is_active"] = bool(body["is_active"])

        if update_data:
            admin.table("paths").update(update_data).eq("id", path_id).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/paths/{path_id}")
async def admin_delete_path(path_id: str, request: Request):
    try:
        await _check_admin(request)
        admin = get_supabase_admin()
        admin.table("paths").delete().eq("id", path_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))