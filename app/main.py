from fastapi import FastAPI

from app.routes import auth, formations, history, marketplace, network, pages, payments

app = FastAPI(title="TriBoost", version="1.0.0")

# ============================================================
# PAGES HTML
# ============================================================
app.include_router(pages.router, tags=["Pages"])

# ============================================================
# API
# ============================================================
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(history.router, prefix="/api/history", tags=["History"])
app.include_router(formations.router, prefix="/api/formations", tags=["Formations"])