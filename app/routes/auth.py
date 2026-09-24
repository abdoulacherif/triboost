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
                    "referral_code": payload.referral_code,
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

        return {
            "success": True,
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in,
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "full_name": response.user.user_metadata.get("full_name", ""),
            },
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")