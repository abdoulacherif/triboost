from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="TriBoost", version="1.0.0")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# ===== ROUTES =====
# Voici les routes publiques — c'est ÇA qui manquait

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user_initial": "A",
            "user_short": "abdo...",
            "user_name": "abdoula",
            "followers_count": 147,
            "is_subscribed": True,
            "balance_fcfa": 1048,
            "principal_fcfa": 1048,
            "crypto_usd": "0.00",
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok", "app": "TriBoost"}