from fastapi import HTTPException
from supabase import Client, create_client

from app.core.config import settings


def get_supabase() -> Client:
    """Retourne une instance Supabase ou lève une erreur si non configuré."""
    if not settings.is_configured:
        raise HTTPException(
            status_code=500,
            detail="Supabase non configuré (SUPABASE_URL / SUPABASE_ANON_KEY manquants)",
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)