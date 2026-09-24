from fastapi import HTTPException
from supabase import Client, create_client

from app.core.config import settings


# ============================================================
# CLIENT ANON (pour authentification)
# ============================================================
def get_supabase() -> Client:
    """Client Supabase avec la clé anonyme (pour l'auth)."""
    if not settings.is_configured:
        raise HTTPException(
            status_code=500,
            detail="Supabase non configuré (SUPABASE_URL / SUPABASE_ANON_KEY manquants)",
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)


# ============================================================
# CLIENT ADMIN (bypass RLS, uniquement côté backend sécurisé)
# ============================================================
def get_supabase_admin() -> Client:
    """
    Client Supabase avec la clé service_role.
    ⚠️ Bypass RLS — à utiliser UNIQUEMENT après avoir vérifié l'utilisateur.
    """
    service_key = getattr(settings, "SUPABASE_SERVICE_ROLE_KEY", "")
    if not service_key:
        # Fallback : utiliser le client anon si la clé admin n'est pas configurée
        print("[WARN] SUPABASE_SERVICE_ROLE_KEY non configurée, utilisation de la clé anon")
        return get_supabase()

    return create_client(settings.SUPABASE_URL, service_key)