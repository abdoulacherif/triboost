from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.templates.dashboard import HTML_DASHBOARD
from app.templates.login import HTML_LOGIN
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


@router.get("/health")
async def health():
    return {"status": "ok", "app": "TriBoost"}