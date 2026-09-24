from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.templates import templates

router = APIRouter()


def _render(request: Request, template: str, context: dict | None = None) -> HTMLResponse:
    """Helper pour rendre un template avec contexte commun."""
    base_context = {
        "request": request,
        "app_name": "TriBoost",
        "user": getattr(request.state, "user", None),
    }
    if context:
        base_context.update(context)
    return templates.TemplateResponse(template, base_context)


# ===== AUTH =====
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse(url="/login")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return _render(request, "login.html")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return _render(request, "register.html", {"referral_code": request.query_params.get("ref", "")})


@router.get("/activate", response_class=HTMLResponse)
async def activate_page(request: Request):
    return _render(request, "activate.html")


# ===== APP =====
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    # Données fictives pour l'instant — seront remplacées par l'API
    context = {
        "balance_fcfa": 1048,
        "principal_fcfa": 1048,
        "crypto_usd": 0.00,
        "user_name": "abdoula",
        "user_short": "abdo...",
        "followers_count": 147,
        "is_subscribed": True,
    }
    return _render(request, "dashboard.html", context)


@router.get("/network", response_class=HTMLResponse)
async def network_page(request: Request):
    return _render(request, "network.html")


@router.get("/commissions", response_class=HTMLResponse)
async def commissions_page(request: Request):
    return _render(request, "commissions.html")


@router.get("/payments", response_class=HTMLResponse)
async def payments_page(request: Request):
    return _render(request, "payments.html")