from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.templates.activation import HTML_ACTIVATION
from app.templates.activation_success import HTML_ACTIVATION_SUCCESS
from app.templates.affilie import HTML_AFFILIE
from app.templates.dashboard import HTML_DASHBOARD
from app.templates.historique import HTML_HISTORIQUE
from app.templates.login import HTML_LOGIN
from app.templates.marche import HTML_MARCHE
from app.templates.placeholder import (
    ICON_AFFAIRE,
    ICON_BOOST,
    ICON_BOUTIQUE,
    ICON_CHAT,
    ICON_COMMISSIONS,
    ICON_FORMATION,
    ICON_PAIEMENTS,
    ICON_SHOP,
    ICON_TACHE,
    ICON_TOURNER,
    make_placeholder,
)
from app.templates.register import HTML_REGISTER

router = APIRouter()


# ============================================================
# AUTH PAGES
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
# APP PAGES
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
    return HTML_HISTORIQUE


# ============================================================
# PLACEHOLDERS (menu burger + services)
# ============================================================
@router.get("/affaire", response_class=HTMLResponse)
async def affaire_page():
    return make_placeholder(
        "Affaire",
        ICON_AFFAIRE,
        "Découvrez les opportunités business et les partenariats TriBoost.",
        "green",
    )


@router.get("/tache", response_class=HTMLResponse)
async def tache_page():
    return make_placeholder(
        "Tâche",
        ICON_TACHE,
        "Accomplissez des missions simples et gagnez des bonus.",
        "blue",
    )


@router.get("/tourner", response_class=HTMLResponse)
async def tourner_page():
    return make_placeholder(
        "Tourner",
        ICON_TOURNER,
        "Faites tourner la roue et tentez de gagner des récompenses.",
        "purple",
    )


@router.get("/formation", response_class=HTMLResponse)
async def formation_page():
    return make_placeholder(
        "Formation",
        ICON_FORMATION,
        "Apprenez les stratégies gagnantes pour développer votre réseau.",
        "orange",
    )


@router.get("/shop", response_class=HTMLResponse)
async def shop_page():
    return make_placeholder(
        "Shop",
        ICON_SHOP,
        "Découvrez tous les produits et services TriBoost.",
        "teal",
    )


@router.get("/boost", response_class=HTMLResponse)
async def boost_page():
    return make_placeholder(
        "Boost",
        ICON_BOOST,
        "Boostez vos gains et accélérez votre progression.",
        "gold",
    )


@router.get("/boutique", response_class=HTMLResponse)
async def boutique_page():
    return make_placeholder(
        "Boutique",
        ICON_BOUTIQUE,
        "Achetez et vendez vos produits dans la boutique TriBoost.",
        "orange",
    )


@router.get("/paiements", response_class=HTMLResponse)
async def paiements_page():
    return make_placeholder(
        "Paiements",
        ICON_PAIEMENTS,
        "Gérez vos retraits Mobile Money et vos historiques de paiement.",
        "green",
    )


@router.get("/chat", response_class=HTMLResponse)
async def chat_page():
    return make_placeholder(
        "Chat",
        ICON_CHAT,
        "Discutez avec votre équipe et votre réseau.",
        "blue",
    )


# ============================================================
# HEALTH
# ============================================================
@router.get("/health")
async def health():
    return {"status": "ok", "app": "TriBoost"}