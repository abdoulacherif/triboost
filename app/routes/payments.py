import time
import json

from fastapi import APIRouter, HTTPException, Request

from app.core.config import settings
from app.core.supabase_client import get_supabase, get_supabase_admin
from app.integrations.leekpay import (
    create_checkout,
    get_checkout_status,
    verify_webhook_signature,
)

router = APIRouter()


# ============================================================
# INITIER UN PAIEMENT D'ACTIVATION (3600 F)
# ============================================================
@router.post("/initiate")
async def initiate_payment(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        body = await request.json()

        phone = (body.get("phone") or "").strip()
        country = (body.get("country") or "CM").strip()

        if not phone:
            raise HTTPException(status_code=400, detail="Numéro de téléphone requis")

        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user_response.user.id
        user_email = user_response.user.email
        user_meta = user_response.user.user_metadata or {}

        admin = get_supabase_admin()
        profile_result = admin.table("profiles").select("full_name, is_activated").eq("id", user_id).execute()

        profile_data = None
        if profile_result.data and len(profile_result.data) > 0:
            profile_data = profile_result.data[0]

        if not profile_data:
            new_code = "TB" + user_id[:6].upper().replace("-", "")
            try:
                insert = admin.table("profiles").insert({
                    "id": user_id,
                    "full_name": user_meta.get("full_name", ""),
                    "phone": user_meta.get("phone", ""),
                    "country": user_meta.get("country", ""),
                    "referral_code": new_code,
                    "is_activated": False,
                    "wallet_balance": 0,
                    "total_earned": 0,
                }).execute()
                if insert.data and len(insert.data) > 0:
                    profile_data = insert.data[0]
                else:
                    profile_data = {"full_name": "", "is_activated": False}
            except Exception as e:
                print(f"[PAYMENT] Erreur création profil: {e}")
                profile_data = {"full_name": "", "is_activated": False}

        if profile_data.get("is_activated"):
            raise HTTPException(status_code=400, detail="Compte déjà activé")

        reference = f"TRIBOOST-{user_id[:8]}-{int(time.time())}"

        checkout = await create_checkout(
            amount=3600,
            currency="XOF",
            description="Activation compte TriBoost",
            return_url=f"{settings.BASE_URL}/activation-success",
            cancel_url=f"{settings.BASE_URL}/activation",
            customer_email=user_email,
            customer_name=profile_data.get("full_name", ""),
            customer_phone=phone,
            metadata={"user_id": user_id, "reference": reference, "country": country},
        )

        try:
            admin.table("activations").insert({
                "user_id": user_id,
                "amount": 3600,
                "payment_method": "leekpay",
                "payment_reference": checkout.get("id"),
                "status": "pending",
            }).execute()
        except Exception as e:
            print(f"[PAYMENT] Erreur enregistrement activation: {e}")

        return {
            "success": True,
            "payment_url": checkout.get("payment_url"),
            "checkout_id": checkout.get("id"),
            "reference": reference,
            "expires_at": checkout.get("expires_at"),
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[PAYMENT] Erreur initiate: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# RETRAIT
# ============================================================
@router.post("/withdraw")
async def create_withdrawal(request: Request):
    """Crée une demande de retrait (min 2000 F)."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        body = await request.json()

        amount = float(body.get("amount") or 0)
        country = (body.get("country") or "").strip()
        operator = (body.get("operator") or "").strip()
        phone = (body.get("phone") or "").strip()
        full_name = (body.get("full_name") or "").strip()

        if amount < 2000:
            raise HTTPException(status_code=400, detail="Montant minimum : 2 000 FCFA")
        if not country or not operator or not phone or not full_name:
            raise HTTPException(status_code=400, detail="Tous les champs sont obligatoires")

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

        result = admin.rpc("create_withdrawal", {
            "p_user_id": user_id,
            "p_amount": amount,
            "p_country": country,
            "p_operator": operator,
            "p_phone": phone,
            "p_full_name": full_name,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        if not result.data.get("success"):
            raise HTTPException(status_code=400, detail=result.data.get("message", "Erreur"))

        return {"success": True, "result": result.data}

    except HTTPException:
        raise
    except Exception as e:
        print(f"[PAYMENT] Erreur withdrawal: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MES RETRAITS
# ============================================================
@router.get("/withdrawals")
async def my_withdrawals(request: Request):
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
        result = admin.table("withdrawals")\
            .select("*")\
            .eq("user_id", user_response.user.id)\
            .order("created_at", desc=True)\
            .execute()

        return {"success": True, "withdrawals": result.data or []}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# RECHARGE
# ============================================================
@router.post("/recharge")
async def create_recharge(request: Request):
    """Crée une recharge via LeekPay (min 1000 F)."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        body = await request.json()

        amount = float(body.get("amount") or 0)
        country = (body.get("country") or "").strip()
        operator = (body.get("operator") or "").strip()
        phone = (body.get("phone") or "").strip()
        full_name = (body.get("full_name") or "").strip()

        if amount < 1000:
            raise HTTPException(status_code=400, detail="Montant minimum : 1 000 FCFA")
        if not country or not operator or not phone or not full_name:
            raise HTTPException(status_code=400, detail="Tous les champs sont obligatoires")

        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user_response.user.id
        user_email = user_response.user.email
        admin = get_supabase_admin()

        # Vérifier activation
        profile = admin.table("profiles").select("is_activated").eq("id", user_id).execute()
        raw = profile.data[0].get("is_activated") if profile.data else False
        is_activated = raw is True or raw == "true" or raw == 1 or raw == "1"
        if not is_activated:
            raise HTTPException(status_code=403, detail="Compte non activé")

        # Créer checkout LeekPay
        reference = f"RECHARGE-{user_id[:8]}-{int(time.time())}"

        checkout = await create_checkout(
            amount=int(amount),
            currency="XOF",
            description="Recharge wallet TriBoost",
            return_url=f"{settings.BASE_URL}/paiements",
            cancel_url=f"{settings.BASE_URL}/paiements",
            customer_email=user_email,
            customer_name=full_name,
            customer_phone=phone,
            metadata={
                "user_id": user_id,
                "reference": reference,
                "type": "recharge",
                "country": country,
                "operator": operator,
            },
        )

        # Enregistrer la recharge
        admin.rpc("create_recharge", {
            "p_user_id": user_id,
            "p_amount": amount,
            "p_country": country,
            "p_operator": operator,
            "p_phone": phone,
            "p_full_name": full_name,
            "p_checkout_id": checkout.get("id"),
        }).execute()

        return {
            "success": True,
            "payment_url": checkout.get("payment_url"),
            "checkout_id": checkout.get("id"),
            "reference": reference,
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[PAYMENT] Erreur recharge: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MES RECHARGES
# ============================================================
@router.get("/recharges")
async def my_recharges(request: Request):
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
        result = admin.table("recharges")\
            .select("*")\
            .eq("user_id", user_response.user.id)\
            .order("created_at", desc=True)\
            .execute()

        return {"success": True, "recharges": result.data or []}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# STATUT PAIEMENT (polling)
# ============================================================
@router.get("/status/{checkout_id}")
async def payment_status(checkout_id: str, request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        status_data = await get_checkout_status(checkout_id)
        status = status_data.get("status")

        admin = get_supabase_admin()

        if status == "paid":
            # Vérifier si c'est une activation ou une recharge
            act = admin.table("activations").select("id").eq("payment_reference", checkout_id).execute()
            if act.data and len(act.data) > 0:
                admin.rpc("activate_account", {
                    "p_user_id": user_response.user.id,
                    "p_payment_method": "leekpay",
                    "p_payment_reference": checkout_id,
                }).execute()
                admin.table("activations").update({"status": "completed"}).eq("payment_reference", checkout_id).execute()
            else:
                admin.rpc("confirm_recharge", {"p_checkout_id": checkout_id}).execute()

        return {"success": True, "status": status, "data": status_data}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# WEBHOOK LEEKPAY
# ============================================================
@router.post("/webhook")
async def leekpay_webhook(request: Request):
    try:
        body_bytes = await request.body()
        signature = request.headers.get("X-LeekPay-Signature", "")
        event_header = request.headers.get("X-LeekPay-Event", "")

        print(f"[WEBHOOK] event={event_header}, sig={'oui' if signature else 'non'}")

        if not verify_webhook_signature(body_bytes, signature):
            print("[WEBHOOK] ⚠️ Signature invalide")
            raise HTTPException(status_code=401, detail="Signature invalide")

        payload = json.loads(body_bytes)
        data = payload.get("data") or payload
        status = data.get("status")
        checkout_id = data.get("checkout_id") or data.get("transaction_id")
        metadata = data.get("metadata") or {}
        user_id = metadata.get("user_id")

        print(f"[WEBHOOK] status={status}, checkout={checkout_id}, user={user_id}")

        if status == "paid":
            admin = get_supabase_admin()

            if not user_id and checkout_id:
                act = admin.table("activations").select("user_id").eq("payment_reference", checkout_id).eq("status", "pending").execute()
                if act.data and len(act.data) > 0:
                    user_id = act.data[0]["user_id"]

            if user_id:
                try:
                    # Vérifier si c'est une activation
                    is_activation = metadata.get("reference", "").startswith("TRIBOOST-")
                    if is_activation:
                        admin.rpc("activate_account", {
                            "p_user_id": user_id,
                            "p_payment_method": "leekpay",
                            "p_payment_reference": checkout_id,
                        }).execute()
                        admin.table("activations").update({"status": "completed"}).eq("payment_reference", checkout_id).execute()
                    else:
                        admin.rpc("confirm_recharge", {"p_checkout_id": checkout_id}).execute()
                    print(f"[WEBHOOK] ✅ Traité pour {user_id}")
                except Exception as e:
                    print(f"[WEBHOOK] Erreur: {e}")

        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        print(f"[WEBHOOK] ❌ Erreur: {e}")
        return {"success": False, "error": str(e)}