from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.templates.activation import HTML_ACTIVATION
from app.templates.affilie import HTML_AFFILIE
from app.templates.dashboard import HTML_DASHBOARD
from app.templates.login import HTML_LOGIN
from app.templates.marche import HTML_MARCHE
from app.templates.placeholder import (
    ICON_AFFAIRE, ICON_BOOST, ICON_BOUTIQUE, ICON_CHAT,
    ICON_COMMISSIONS, ICON_FORMATION, ICON_PAIEMENTS,
    ICON_SHOP, ICON_TACHE, ICON_TOURNER, make_placeholder,
)
from app.templates.register import HTML_REGISTER

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home():
    return HTML_LOGIN


@router.get("/login", response_class=HTMLResponse)
async def login_page():
    return HTML_LOGIN


@router.get("/register", response_class=HTMLResponse)
async def register_page():
    return HTML_REGISTER


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    return HTML_DASHBOARD


@router.get("/activation", response_class=HTMLResponse)
async def activation_page():
    return HTML_ACTIVATION


@router.get("/marche", response_class=HTMLResponse)
async def marche_page():
    return HTML_MARCHE


@router.get("/affilie", response_class=HTMLResponse)
async def affilie_page():
    return HTML_AFFILIE


# Placeholders
@router.get("/affaire", response_class=HTMLResponse)
async def affaire_page():
    return make_placeholder("Affaire", ICON_AFFAIRE, "Découvrez les opportunités business.", "green")


@router.get("/tache", response_class=HTMLResponse)
async def tache_page():
    return make_placeholder("Tâche", ICON_TACHE, "Accomplissez des missions.", "blue")


@router.get("/tourner", response_class=HTMLResponse)
async def tourner_page():
    return make_placeholder("Tourner", ICON_TOURNER, "Faites tourner la roue.", "purple")


@router.get("/formation", response_class=HTMLResponse)
async def formation_page():
    return make_placeholder("Formation", ICON_FORMATION, "Apprenez les stratégies gagnantes.", "orange")


@router.get("/shop", response_class=HTMLResponse)
async def shop_page():
    return make_placeholder("Shop", ICON_SHOP, "Produits et services TriBoost.", "teal")


@router.get("/boost", response_class=HTMLResponse)
async def boost_page():
    return make_placeholder("Boost", ICON_BOOST, "Boostez vos gains.", "gold")


@router.get("/boutique", response_class=HTMLResponse)
async def boutique_page():
    return make_placeholder("Boutique", ICON_BOUTIQUE, "Achetez et vendez vos produits.", "orange")


@router.get("/commissions", response_class=HTMLResponse)
async def commissions_page():
    return make_placeholder("Commissions", ICON_COMMISSIONS, "Suivez vos commissions.", "red")


@router.get("/paiements", response_class=HTMLResponse)
async def paiements_page():
    return make_placeholder("Paiements", ICON_PAIEMENTS, "Retraits Mobile Money.", "green")


@router.get("/chat", response_class=HTMLResponse)
async def chat_page():
    return make_placeholder("Chat", ICON_CHAT, "Discutez avec votre équipe.", "blue")


@router.get("/health")
async def health():
    return {"status": "ok", "app": "TriBoost"}