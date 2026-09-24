import sys
from pathlib import Path

# Permet à Vercel de trouver le dossier /app
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.main import app  # noqa: E402

# Vercel cherche la variable "app" ou "handler"
handler = app