from fastapi import FastAPI

from app.routes import auth, marketplace, network, pages, payments

app = FastAPI(title="TriBoost", version="1.0.0")

app.include_router(pages.router, tags=["Pages"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])