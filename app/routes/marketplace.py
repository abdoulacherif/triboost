import base64
import uuid

from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin
from app.models.schemas import MarketItemCreate

router = APIRouter()


# ============================================================
# LISTER LES ANNONCES
# ============================================================
@router.get("/items")
async def list_items(
    category: str | None = None,
    search: str | None = None,
    limit: int = 50,
):
    try:
        admin = get_supabase_admin()
        query = (
            admin.table("marketplace_items")
            .select("id, title, description, price, category, city, whatsapp, image_url, views, created_at, user_id")
            .eq("is_active", True)
            .order("created_at", desc=True)
            .limit(limit)
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
                or s in (i.get("city", "") or "").lower()
            ]

        return {"success": True, "items": items, "count": len(items)}
    except Exception as e:
        print(f"[MARKET] Erreur list: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# CRÉER UNE ANNONCE (nécessite compte activé)
# ============================================================
@router.post("/items")
async def create_item(payload: MarketItemCreate, request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")

        # 1️⃣ Vérifier l'utilisateur avec le client ANON
        supabase_anon = get_supabase()
        try:
            user_response = supabase_anon.auth.get_user(token)
        except Exception:
            raise HTTPException(status_code=401, detail="Token invalide")

        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user_response.user.id

        # 2️⃣ Vérifier l'activation avec le client ADMIN (bypass RLS)
        admin = get_supabase_admin()
        profile_result = (
            admin.table("profiles")
            .select("is_activated")
            .eq("id", user_id)
            .execute()
        )

        is_activated = False
        if profile_result.data and len(profile_result.data) > 0:
            raw = profile_result.data[0].get("is_activated")
            is_activated = (
                raw is True or raw == "true" or raw == 1 or raw == "1"
            )

        if not is_activated:
            raise HTTPException(
                status_code=403,
                detail="Compte non activé. Activez pour 3 600 FCFA."
            )

        # 3️⃣ Upload image si fournie
        image_url = None
        if payload.image_base64:
            try:
                header, b64data = payload.image_base64.split(",", 1)
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

                filename = f"{user_id}/{uuid.uuid4().hex}.{ext}"
                admin.storage.from_("marketplace").upload(
                    path=filename,
                    file=img_bytes,
                    file_options={"content-type": f"image/{ext}"},
                )
                image_url = admin.storage.from_("marketplace").get_public_url(filename)
            except HTTPException:
                raise
            except Exception as e:
                print(f"[MARKET] Erreur upload image: {e}")

        # 4️⃣ Insérer l'annonce
        insert = admin.table("marketplace_items").insert({
            "user_id": user_id,
            "title": payload.title,
            "description": payload.description,
            "price": payload.price,
            "category": payload.category,
            "city": payload.city,
            "whatsapp": payload.whatsapp,
            "image_url": image_url,
        }).execute()

        if not insert.data or len(insert.data) == 0:
            raise HTTPException(status_code=400, detail="Erreur lors de la création")

        return {"success": True, "item": insert.data[0]}

    except HTTPException:
        raise
    except Exception as e:
        print(f"[MARKET] Erreur create: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SUPPRIMER UNE ANNONCE
# ============================================================
@router.delete("/items/{item_id}")
async def delete_item(item_id: str, request: Request):
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
        admin.table("marketplace_items").delete()\
            .eq("id", item_id)\
            .eq("user_id", user_response.user.id)\
            .execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[MARKET] Erreur delete: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MES ANNONCES
# ============================================================
@router.get("/my-items")
async def my_items(request: Request):
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
            admin.table("marketplace_items")
            .select("*")
            .eq("user_id", user_response.user.id)
            .order("created_at", desc=True)
            .execute()
        )

        return {"success": True, "items": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[MARKET] Erreur my-items: {e}")
        raise HTTPException(status_code=400, detail=str(e))