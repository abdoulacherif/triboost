from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.templates.activation import HTML_ACTIVATION
from app.templates.activation_success import HTML_ACTIVATION_SUCCESS
from app.templates.affaire import HTML_AFFAIRE
from app.templates.affilie import HTML_AFFILIE
from app.templates.boost import HTML_BOOST
from app.templates.boutique import HTML_BOUTIQUE
from app.templates.commissions import HTML_COMMISSIONS
from app.templates.dashboard import HTML_DASHBOARD
from app.templates.formation_detail import HTML_FORMATION_DETAIL
from app.templates.historique import HTML_HISTORIQUE
from app.templates.login import HTML_LOGIN
from app.templates.marche import HTML_MARCHE
from app.templates.paiements import HTML_PAIEMENTS
from app.templates.placeholder import (
    ICON_CHAT,
    ICON_FORMATION,
    ICON_SHOP,
    ICON_TOURNER,
    make_placeholder,
)
from app.templates.register import HTML_REGISTER
from app.templates.taches import HTML_TACHES

router = APIRouter()


# ============================================================
# AUTH
# ============================================================
@router.get("/", response_class=HTMLResponse)
async def home():
    return HTML_LOGIN


@router.get("/login", response_class=HTMLResponse)
async def login_page():
    return HTML_LOGIN


@router.get("/register", response_class=HTMLResponse)
async def register_page():
    return HTML_REGISTER


# ============================================================
# PAGES PRINCIPALES
# ============================================================
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    return HTML_DASHBOARD


@router.get("/activation", response_class=HTMLResponse)
async def activation_page():
    return HTML_ACTIVATION


@router.get("/activation-success", response_class=HTMLResponse)
async def activation_success_page():
    return HTML_ACTIVATION_SUCCESS


@router.get("/marche", response_class=HTMLResponse)
async def marche_page():
    return HTML_MARCHE


@router.get("/affilie", response_class=HTMLResponse)
async def affilie_page():
    return HTML_AFFILIE


@router.get("/historique", response_class=HTMLResponse)
async def historique_page():
    return HTML_HISTORIQUE


@router.get("/commissions", response_class=HTMLResponse)
async def commissions_page():
    return HTML_COMMISSIONS


@router.get("/boutique", response_class=HTMLResponse)
async def boutique_page():
    return HTML_BOUTIQUE


@router.get("/boutique/{formation_id}", response_class=HTMLResponse)
async def formation_detail_page(formation_id: str):
    return HTML_FORMATION_DETAIL


@router.get("/tache", response_class=HTMLResponse)
async def tache_page():
    return HTML_TACHES


@router.get("/affaire", response_class=HTMLResponse)
async def affaire_page():
    return HTML_AFFAIRE


@router.get("/boost", response_class=HTMLResponse)
async def boost_page():
    return HTML_BOOST


# ============================================================
# PAIEMENTS
# ============================================================
@router.get("/paiements", response_class=HTMLResponse)
async def paiements_page():
    return HTML_PAIEMENTS


# ============================================================
# PLACEHOLDERS (⚠️ NE JAMAIS METTRE /paiements ICI)
# ============================================================
@router.get("/tourner", response_class=HTMLResponse)
async def tourner_page():
    return make_placeholder("Tourner", ICON_TOURNER, "Roue de la chance.", "purple")


@router.get("/formation", response_class=HTMLResponse)
async def formation_page():
    return make_placeholder("Formation", ICON_FORMATION, "Formations TriBoost.", "orange")


@router.get("/shop", response_class=HTMLResponse)
async def shop_page():
    return make_placeholder("Shop", ICON_SHOP, "Produits & services.", "teal")


@router.get("/chat", response_class=HTMLResponse)
async def chat_page():
    return make_placeholder("Chat", ICON_CHAT, "Discutez avec votre équipe.", "blue")


# ============================================================
# HEALTH
# ============================================================
@router.get("/health")
async def health():
    return {"status": "ok", "app": "TriBoost"}