from fastapi import FastAPI

from app.routes import auth, marketplace, pages

app = FastAPI(title="TriBoost", version="1.0.0")

# Routes HTML (pages)
app.include_router(pages.router, tags=["Pages"])

# Routes API
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])