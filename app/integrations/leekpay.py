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

    url = f"{settings.LEEKPAY_API_URL}/checkout"
    print(f"[LEEKPAY] POST {url}")
    print(f"[LEEKPAY] Amount: {amount} {currency}")
    print(f"[LEEKPAY] Secret key (debut): {settings.LEEKPAY_SECRET_KEY[:15]}...")

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
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(follow_redirects=False, timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)

            print(f"[LEEKPAY] Status: {response.status_code}")
            print(f"[LEEKPAY] Response (200 char): {response.text[:200]}")

            # Si redirection → mauvais endpoint
            if response.status_code in (301, 302, 303, 307, 308):
                location = response.headers.get("location", "?")
                print(f"[LEEKPAY] REDIRECTION vers: {location}")
                raise HTTPException(
                    status_code=500,
                    detail=f"LeekPay redirige vers {location}. Vérifie l'URL API.",
                )

            # Si HTML au lieu de JSON
            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type:
                print(f"[LEEKPAY] Content-Type: {content_type}")
                print(f"[LEEKPAY] Body HTML: {response.text[:300]}")
                raise HTTPException(
                    status_code=500,
                    detail=f"LeekPay renvoie du HTML au lieu de JSON. URL: {url}",
                )

            if response.status_code not in (200, 201):
                raise HTTPException(
                    status_code=400,
                    detail=f"LeekPay erreur {response.status_code}: {response.text[:200]}",
                )

            data = response.json()
            return data.get("data", data)

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LeekPay timeout")
    except HTTPException:
        raise
    except Exception as e:
        print(f"[LEEKPAY] Exception: {e}")
        raise HTTPException(status_code=500, detail=f"LeekPay erreur: {str(e)}")


# ============================================================
# VÉRIFIER LE STATUT D'UN CHECKOUT
# ============================================================
async def get_checkout_status(checkout_id: str) -> dict:
    """Vérifie le statut d'un checkout LeekPay."""
    if not settings.is_leekpay_configured:
        raise HTTPException(status_code=500, detail="LeekPay non configuré")

    url = f"{settings.LEEKPAY_API_URL}/checkout/{checkout_id}"
    headers = {
        "Authorization": f"Bearer {settings.LEEKPAY_SECRET_KEY}",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(follow_redirects=False, timeout=15) as client:
        response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Erreur LeekPay")

        return response.json().get("data", {})


# ============================================================
# VÉRIFIER LA SIGNATURE DU WEBHOOK
# ============================================================
def verify_webhook_signature(payload_body: bytes, signature: str) -> bool:
    """Vérifie la signature HMAC SHA256 du webhook LeekPay."""
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