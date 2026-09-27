"""
Client Supabase partagé pour toute l'application.
Utilisé par les routes FastAPI pour interagir avec la base Supabase.
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env (utile en local)
load_dotenv()

# Récupération des variables d'environnement
SUPABASE_URL: str | None = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str | None = os.environ.get("SUPABASE_KEY")

# Vérification au démarrage (aide au debug)
if not SUPABASE_URL:
    raise RuntimeError(
        "❌ SUPABASE_URL manquant. "
        "Ajoute-le dans .env (local) et dans Vercel → Settings → Environment Variables."
    )
if not SUPABASE_KEY:
    raise RuntimeError(
        "❌ SUPABASE_KEY manquant. "
        "Ajoute-le dans .env (local) et dans Vercel → Settings → Environment Variables."
    )

# Création du client unique (singleton)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Optionnel : un client admin avec la service_role key (si tu en as besoin)
# ⚠️ Ne jamais exposer la service_role key côté client !
SUPABASE_SERVICE_KEY: str | None = os.environ.get("SUPABASE_SERVICE_KEY")

if SUPABASE_SERVICE_KEY:
    supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
else:
    supabase_admin = supabase  # fallback