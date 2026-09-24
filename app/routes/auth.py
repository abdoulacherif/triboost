from fastapi import APIRouter, HTTPException

from app.core.supabase_client import get_supabase
from app.models.schemas import LoginRequest, RegisterRequest

router = APIRouter()


@router.post("/register")
async def api_register(payload: RegisterRequest):
    """Crée un compte via Supabase Auth."""
    try:
        supabase = get_supabase()
        response = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password,
            "options": {
                "data": {
                    "full_name": payload.full_name,
                    "phone": payload.phone,
                    "country": payload.country,
                    "referral_code": payload.referral_code or "",
                }
            },
        })

        if response.user is None:
            raise HTTPException(status_code=400, detail="Erreur lors de la création")

        return {
            "success": True,
            "message": "Compte créé. Vérifiez votre email.",
            "user": {"id": response.user.id, "email": response.user.email},
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def api_login(payload: LoginRequest):
    """Connexion via Supabase Auth."""
    try:
        supabase = get_supabase()
        response = supabase.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password,
        })

        if response.session is None:
            raise HTTPException(status_code=401, detail="Identifiants invalides")

        # Récupérer le profil
        profile_data = None
        try:
            profile = (
                supabase.table("profiles")
                .select("*")
                .eq("id", response.user.id)
                .single()
                .execute()
            )
            profile_data = profile.data
        except Exception:
            profile_data = None

        return {
            "success": True,
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in,
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "full_name": response.user.user_metadata.get("full_name", ""),
                "referral_code": profile_data.get("referral_code") if profile_data else None,
            },
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")


@router.get("/check-referral/{code}")
async def check_referral(code: str):
    """Vérifie si un code de parrainage existe."""
    try:
        supabase = get_supabase()
        result = supabase.rpc(
            "check_referral_code",
            {"code": code.upper().strip()}
        ).execute()

        if result.data and len(result.data) > 0:
            referrer = result.data[0]
            return {
                "valid": True,
                "full_name": referrer.get("full_name", ""),
                "country": referrer.get("country", ""),
            }
        return {"valid": False}
    except Exception:
        return {"valid": False}