from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin
from app.models.schemas import LoginRequest, RegisterRequest

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

        user_id = response.user.id
        user_email = response.user.email
        user_meta = response.user.user_metadata or {}

        # Lire le profil avec le client ADMIN (bypass RLS)
        profile_data = None
        try:
            admin = get_supabase_admin()
            profile = (
                admin.table("profiles")
                .select("*")
                .eq("id", user_id)
                .execute()
            )
            if profile.data and len(profile.data) > 0:
                profile_data = profile.data[0]
        except Exception as e:
            print(f"[LOGIN] Erreur récupération profil: {e}")

        # Si pas de profil → le créer via admin
        if not profile_data:
            new_code = "TB" + user_id[:6].upper().replace("-", "")
            try:
                admin = get_supabase_admin()
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
            except Exception as e:
                print(f"[LOGIN] Erreur création profil: {e}")

        return {
            "success": True,
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in,
            "user": {
                "id": user_id,
                "email": user_email,
                "full_name": user_meta.get("full_name", ""),
                "referral_code": profile_data.get("referral_code") if profile_data else None,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[LOGIN] Erreur: {e}")
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")


# ============================================================
# VÉRIFICATION CODE PARRAIN
# ============================================================
@router.get("/check-referral/{code}")
async def check_referral(code: str):
    """Vérifie si un code de parrainage existe."""
    try:
        admin = get_supabase_admin()
        result = admin.rpc(
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
    except Exception as e:
        print(f"[CHECK-REF] Erreur: {e}")
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

        # 1️⃣ Vérifier l'utilisateur avec le client ANON
        supabase_anon = get_supabase()
        try:
            user_response = supabase_anon.auth.get_user(token)
        except Exception:
            raise HTTPException(status_code=401, detail="Token invalide")

        if not user_response.user or user_response.user.id != user_id:
            raise HTTPException(status_code=403, detail="Accès refusé")

        user = user_response.user
        user_meta = user.user_metadata or {}

        # 2️⃣ Lire le profil avec le client ADMIN (bypass RLS)
        admin = get_supabase_admin()
        result = (
            admin.table("profiles")
            .select("*")
            .eq("id", user_id)
            .execute()
        )

        if result.data and len(result.data) > 0:
            print(f"[PROFILE] ✅ Profil réel trouvé pour {user_id}")
            return {"success": True, "profile": result.data[0]}

        # 3️⃣ Profil manquant → créer avec le client ADMIN
        print(f"[PROFILE] ⚠️ Profil manquant, création pour {user_id}")
        new_code = "TB" + user_id[:6].upper().replace("-", "")

        try:
            insert = admin.table("profiles").insert({
                "id": user.id,
                "full_name": user_meta.get("full_name", ""),
                "phone": user_meta.get("phone", ""),
                "country": user_meta.get("country", ""),
                "referral_code": new_code,
                "is_activated": False,
                "wallet_balance": 0,
                "total_earned": 0,
            }).execute()

            if insert.data and len(insert.data) > 0:
                print(f"[PROFILE] ✅ Profil créé pour {user_id}")
                return {"success": True, "profile": insert.data[0], "created": True}
        except Exception as e:
            print(f"[PROFILE] ❌ Erreur création: {e}")

        # 4️⃣ Fallback ultime (ne devrait plus arriver)
        print(f"[PROFILE] ⚠️ Fallback virtuel pour {user_id}")
        return {
            "success": True,
            "profile": {
                "id": user.id,
                "full_name": user_meta.get("full_name", ""),
                "phone": user_meta.get("phone", ""),
                "country": user_meta.get("country", ""),
                "referral_code": new_code,
                "is_activated": False,
                "wallet_balance": 0,
                "total_earned": 0,
            },
            "fallback": True,
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[PROFILE] Erreur: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# ACTIVATION MANUELLE (admin / test uniquement)
# ============================================================
@router.post("/activate")
async def activate(request: Request):
    """Active le compte manuellement (⚠️ usage admin / test)."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        body = await request.json()
        payment_method = body.get("payment_method", "manual")
        payment_reference = body.get("payment_reference", "")

        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.rpc(
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