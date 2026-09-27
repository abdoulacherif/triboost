"""
Client Supabase partagé pour toute l'application.

Variables d'environnement attendues (Vercel + .env local) :
    - SUPABASE_URL                 → URL du projet Supabase
    - SUPABASE_ANON_KEY            → clé publique "anon" (utilisée partout)
    - SUPABASE_SERVICE_ROLE_KEY    → clé service_role (⚠️ admin uniquement, ne jamais exposer)
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Charge les variables depuis .env (utile en local uniquement)
load_dotenv()


# ---------------------------------------------------------------------------
# Récupération des variables d'environnement
# ---------------------------------------------------------------------------
SUPABASE_URL: str | None = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY: str | None = os.environ.get("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY: str | None = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")


# ---------------------------------------------------------------------------
# Vérifications au démarrage (aide au debug)
# ---------------------------------------------------------------------------
if not SUPABASE_URL:
    raise RuntimeError(
        "❌ SUPABASE_URL manquant. "
        "Ajoute-le dans .env (local) et dans Vercel → Settings → Environment Variables."
    )

if not SUPABASE_ANON_KEY:
    raise RuntimeError(
        "❌ SUPABASE_ANON_KEY manquant. "
        "Ajoute-le dans .env (local) et dans Vercel → Settings → Environment Variables."
    )


# ---------------------------------------------------------------------------
# Client public (anon) — à utiliser partout dans les routes FastAPI
# ---------------------------------------------------------------------------
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


# ---------------------------------------------------------------------------
# Client admin (service_role) — usage restreint côté serveur uniquement
# ⚠️ Ne JAMAIS exposer cette clé côté client (navigateur/mobile)
# ---------------------------------------------------------------------------
if SUPABASE_SERVICE_ROLE_KEY:
    supabase_admin: Client = create_client(
        SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
    )
else:
    # Fallback : si la clé n'est pas définie, on retombe sur le client public
    supabase_admin = supabase