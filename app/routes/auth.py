from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase
from app.models.schemas import LoginRequest, RegisterRequest

# ⚠️ IMPORTANT : router DOIT être défini AVANT les décorateurs
router = APIRouter()


# ============================================================
# INSCRIPTION
# ============================================================
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


# ============================================================
# CONNEXION
# ============================================================
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


# ============================================================
# VÉRIFICATION CODE PARRAIN
# ============================================================
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


# ============================================================
# PROFIL UTILISATEUR
# ============================================================
@router.get("/profile/{user_id}")
async def get_profile(user_id: str, request: Request):
    """Récupère le profil complet d'un utilisateur."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        supabase = get_supabase()

        # Vérifier l'utilisateur
        user_response = supabase.auth.get_user(token)
        if not user_response.user or user_response.user.id != user_id:
            raise HTTPException(status_code=403, detail="Accès refusé")

        # Récupérer le profil
        result = (
            supabase.table("profiles")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=404, detail="Profil introuvable")

        return {"success": True, "profile": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# ACTIVATION DU COMPTE
# ============================================================
@router.post("/activate")
async def activate(request: Request):
    """Active le compte de l'utilisateur (paiement 3600 FCFA)."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        body = await request.json()
        payment_method = body.get("payment_method", "manual")
        payment_reference = body.get("payment_reference", "")

        supabase = get_supabase()

        # Vérifier l'utilisateur
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        # Activer le compte
        result = supabase.rpc(
            "activate_account",
            {
                "p_user_id": user_response.user.id,
                "p_payment_method": payment_method,
                "p_payment_reference": payment_reference or None,
            }
        ).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Échec de l'activation")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))