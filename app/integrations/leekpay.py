import hashlib
import hmac

import httpx
from fastapi import HTTPException

from app.core.config import settings


# ============================================================
# CRÉER UN CHECKOUT
# ============================================================
async def create_checkout(
    amount: int,
    currency: str = "XOF",
    description: str = "Activation TriBoost",
    return_url: str = "",
    cancel_url: str = "",
    customer_email: str = "",
    customer_name: str = "",
    customer_phone: str = "",
    metadata: dict | None = None,
) -> dict:
    """Crée un checkout LeekPay et retourne l'URL de paiement."""
    if not settings.is_leekpay_configured:
        raise HTTPException(status_code=500, detail="LeekPay non configuré")

    payload = {
        "amount": amount,
        "currency": currency,
        "description": description,
        "return_url": return_url,
        "cancel_url": cancel_url,
        "webhook_url": f"{settings.BASE_URL}/api/payments/webhook",
        "customer_email": customer_email,
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "metadata": metadata or {},
    }

    headers = {
        "Authorization": f"Bearer {settings.LEEKPAY_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.LEEKPAY_API_URL}/checkout",
            json=payload,
            headers=headers,
            timeout=30,
        )

    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=400,
            detail=f"LeekPay erreur: {response.text}",
        )

    data = response.json()
    return data.get("data", {})


# ============================================================
# VÉRIFIER LE STATUT D'UN CHECKOUT
# ============================================================
async def get_checkout_status(checkout_id: str) -> dict:
    """Vérifie le statut d'un checkout LeekPay."""
    if not settings.is_leekpay_configured:
        raise HTTPException(status_code=500, detail="LeekPay non configuré")

    headers = {"Authorization": f"Bearer {settings.LEEKPAY_SECRET_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.LEEKPAY_API_URL}/checkout/{checkout_id}",
            headers=headers,
            timeout=15,
        )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Erreur LeekPay")

    return response.json().get("data", {})


# ============================================================
# VÉRIFIER LA SIGNATURE DU WEBHOOK
# ============================================================
def verify_webhook_signature(payload_body: bytes, signature: str) -> bool:
    """
    Vérifie la signature HMAC SHA256 du webhook LeekPay.
    ⚠️ La clé utilisée est la CLÉ PUBLIQUE (pk_live_xxx).
    """
    if not settings.LEEKPAY_PUBLIC_KEY:
        return False

    if not signature:
        return False

    expected = hmac.new(
        settings.LEEKPAY_PUBLIC_KEY.encode(),
        payload_body,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)