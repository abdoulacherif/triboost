from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# ACHETER UN BOOST
# ============================================================
@router.post("/boost/{item_id}")
async def buy_boost(item_id: str, request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        body = await request.json()
        boost_type = body.get("boost_type")

        if boost_type not in ("24h", "7d", "banner", "notify"):
            raise HTTPException(status_code=400, detail="Type de boost invalide")

        admin = get_supabase_admin()
        result = admin.rpc("purchase_boost", {
            "p_user_id": user.user.id,
            "p_item_id": item_id,
            "p_boost_type": boost_type,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MES BOOSTS
# ============================================================
@router.get("/my-boosts")
async def my_boosts(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.table("boost_purchases").select(
            "*, marketplace_items(title, image_url)"
        ).eq("user_id", user.user.id).order("created_at", desc=True).limit(50).execute()

        return {"success": True, "boosts": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# ENVOYER UN POURBOIRE
# ============================================================
@router.post("/tip")
async def send_tip(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        body = await request.json()
        receiver_id = body.get("receiver_id")
        amount = float(body.get("amount", 0))
        message = (body.get("message") or "").strip()

        if not receiver_id:
            raise HTTPException(status_code=400, detail="Destinataire obligatoire")

        admin = get_supabase_admin()
        result = admin.rpc("send_tip", {
            "p_sender_id": user.user.id,
            "p_receiver_id": receiver_id,
            "p_amount": amount,
            "p_message": message,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# PROFIL PUBLIC
# ============================================================
@router.get("/profile/{user_id}")
async def get_public_profile(user_id: str, request: Request):
    try:
        admin = get_supabase_admin()

        # Profil
        profile = admin.table("profiles").select(
            "id, full_name, country, is_activated, created_at"
        ).eq("id", user_id).execute()

        if not profile.data or len(profile.data) == 0:
            raise HTTPException(status_code=404, detail="Profil introuvable")

        # Stats
        products = admin.table("marketplace_items").select("id").eq("user_id", user_id).eq("is_active", True).execute()
        services = admin.table("digital_services").select("id").eq("user_id", user_id).eq("is_active", True).execute()
        formations = admin.table("formations").select("id").eq("user_id", user_id).execute() if hasattr(admin, 'formations') else type('obj', (), {'data': []})()

        # Pourboires reçus
        tips = admin.table("tips").select("id").eq("receiver_id", user_id).execute()

        total_tips = 0
        try:
            tips_sum = admin.table("tips").select("receiver_gets").eq("receiver_id", user_id).execute()
            total_tips = sum(float(t.get("receiver_gets", 0)) for t in (tips_sum.data or []))
        except Exception:
            pass

        return {
            "success": True,
            "profile": profile.data[0],
            "stats": {
                "products": len(products.data or []),
                "services": len(services.data or []),
                "tips_count": len(tips.data or []),
                "tips_total": total_tips,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))