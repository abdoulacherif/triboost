import base64
import uuid

from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase
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
        supabase = get_supabase()
        query = (
            supabase.table("marketplace_items")
            .select("id, title, description, price, category, city, whatsapp, image_url, views, created_at, user_id")
            .eq("is_active", True)
            .order("created_at", desc=True)
            .limit(limit)
        )

        if category and category != "tous":
            query = query.eq("category", category)

        result = query.execute()
        items = result.data or []

        # Filtrer par recherche côté serveur
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
        supabase = get_supabase()

        # Vérifier l'utilisateur
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")
        user_id = user_response.user.id

        # Vérifier que le compte est activé
        profile = (
            supabase.table("profiles")
            .select("is_activated")
            .eq("id", user_id)
            .single()
            .execute()
        )
        if not profile.data or not profile.data.get("is_activated"):
            raise HTTPException(
                status_code=403,
                detail="Compte non activé. Activez pour 3 600 FCFA."
            )

        # Upload image si fournie
        image_url = None
        if payload.image_base64:
            try:
                # Parse "data:image/jpeg;base64,/9j/4AA..."
                header, b64data = payload.image_base64.split(",", 1)
                ext = "jpg"
                if "png" in header:
                    ext = "png"
                elif "webp" in header:
                    ext = "webp"
                elif "gif" in header:
                    ext = "gif"

                img_bytes = base64.b64decode(b64data)
                # Limite 5 MB
                if len(img_bytes) > 5 * 1024 * 1024:
                    raise HTTPException(status_code=400, detail="Image trop lourde (max 5 MB)")

                filename = f"{user_id}/{uuid.uuid4().hex}.{ext}"
                supabase.storage.from_("marketplace").upload(
                    path=filename,
                    file=img_bytes,
                    file_options={"content-type": f"image/{ext}"},
                )
                image_url = supabase.storage.from_("marketplace").get_public_url(filename)
            except HTTPException:
                raise
            except Exception as e:
                print(f"[MARKET] Erreur upload image: {e}")

        # Insérer l'annonce
        insert = supabase.table("marketplace_items").insert({
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
        supabase = get_supabase()

        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        # Supprimer uniquement si propriétaire
        supabase.table("marketplace_items").delete().eq("id", item_id).eq("user_id", user_response.user.id).execute()

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
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
        supabase = get_supabase()

        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        result = (
            supabase.table("marketplace_items")
            .select("*")
            .eq("user_id", user_response.user.id)
            .order("created_at", desc=True)
            .execute()
        )

        return {"success": True, "items": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))