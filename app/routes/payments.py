import time
import json

from fastapi import APIRouter, HTTPException, Request

from app.core.config import settings
from app.core.supabase_client import get_supabase
from app.integrations.leekpay import (
    create_checkout,
    get_checkout_status,
    verify_webhook_signature,
)

router = APIRouter()


# ============================================================
# INITIER UN PAIEMENT D'ACTIVATION
# ============================================================
@router.post("/initiate")
async def initiate_payment(request: Request):
    """Crée un checkout LeekPay pour l'activation du compte."""
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

        if len(phone) < 8:
            raise HTTPException(status_code=400, detail="Numéro de téléphone invalide")

        supabase = get_supabase()
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user_response.user.id
        user_email = user_response.user.email

        profile = (
            supabase.table("profiles")
            .select("full_name, is_activated")
            .eq("id", user_id)
            .single()
            .execute()
        )

        if not profile.data:
            raise HTTPException(status_code=404, detail="Profil introuvable")

        if profile.data.get("is_activated"):
            raise HTTPException(status_code=400, detail="Compte déjà activé")

        reference = f"TRIBOOST-{user_id[:8]}-{int(time.time())}"

        checkout = await create_checkout(
            amount=3600,
            currency="XOF",
            description="Activation compte TriBoost",
            return_url=f"{settings.BASE_URL}/activation-success",
            cancel_url=f"{settings.BASE_URL}/activation",
            customer_email=user_email,
            customer_name=profile.data.get("full_name", ""),
            customer_phone=phone,
            metadata={
                "user_id": user_id,
                "reference": reference,
                "country": country,
            },
        )

        try:
            supabase.table("activations").insert({
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
# VÉRIFIER LE STATUT D'UN PAIEMENT (Polling)
# ============================================================
@router.get("/status/{checkout_id}")
async def payment_status(checkout_id: str, request: Request):
    """Vérifie le statut d'un checkout LeekPay."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        supabase = get_supabase()
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user_response.user.id

        status_data = await get_checkout_status(checkout_id)
        status = status_data.get("status")

        if status == "paid":
            try:
                supabase.rpc("activate_account", {
                    "p_user_id": user_id,
                    "p_payment_method": "leekpay",
                    "p_payment_reference": checkout_id,
                }).execute()

                supabase.table("activations").update({
                    "status": "completed",
                }).eq("payment_reference", checkout_id).eq("user_id", user_id).execute()

            except Exception as e:
                print(f"[PAYMENT] Erreur activation: {e}")

        elif status in ("failed", "cancelled", "expired"):
            try:
                supabase.table("activations").update({
                    "status": "failed",
                }).eq("payment_reference", checkout_id).eq("user_id", user_id).execute()
            except Exception:
                pass

        return {
            "success": True,
            "status": status,
            "data": status_data,
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[PAYMENT] Erreur status: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# WEBHOOK LEEKPAY
# ============================================================
@router.post("/webhook")
async def leekpay_webhook(request: Request):
    """Reçoit la confirmation de paiement LeekPay."""
    try:
        body_bytes = await request.body()
        signature = request.headers.get("X-LeekPay-Signature", "")
        event_header = request.headers.get("X-LeekPay-Event", "")

        print(f"[WEBHOOK] Reçu: event={event_header}, sig={'oui' if signature else 'non'}")

        if not verify_webhook_signature(body_bytes, signature):
            print("[WEBHOOK] ⚠️ Signature invalide")
            raise HTTPException(status_code=401, detail="Signature invalide")

        payload = json.loads(body_bytes)
        event = payload.get("event") or event_header
        data = payload.get("data") or payload

        status = data.get("status")
        checkout_id = data.get("checkout_id") or data.get("transaction_id")
        metadata = data.get("metadata") or {}
        user_id = metadata.get("user_id")

        print(f"[WEBHOOK] status={status}, checkout={checkout_id}, user={user_id}")

        if status == "paid":
            if not user_id and checkout_id:
                supabase = get_supabase()
                act = (
                    supabase.table("activations")
                    .select("user_id")
                    .eq("payment_reference", checkout_id)
                    .eq("status", "pending")
                    .execute()
                )
                if act.data and len(act.data) > 0:
                    user_id = act.data[0]["user_id"]

            if user_id:
                supabase = get_supabase()
                try:
                    supabase.rpc("activate_account", {
                        "p_user_id": user_id,
                        "p_payment_method": "leekpay",
                        "p_payment_reference": checkout_id,
                    }).execute()

                    supabase.table("activations").update({
                        "status": "completed",
                    }).eq("payment_reference", checkout_id).execute()

                    print(f"[WEBHOOK] ✅ Compte {user_id} activé")
                except Exception as e:
                    print(f"[WEBHOOK] Erreur activation: {e}")

        elif status in ("failed", "cancelled", "expired"):
            if checkout_id:
                try:
                    supabase = get_supabase()
                    supabase.table("activations").update({
                        "status": "failed",
                    }).eq("payment_reference", checkout_id).execute()
                except Exception:
                    pass

        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        print(f"[WEBHOOK] ❌ Erreur: {e}")
        return {"success": False, "error": str(e)}