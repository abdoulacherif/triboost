from fastapi import FastAPI

from app.routes import (
    affaires,
    auth,
    boost,
    formations,
    history,
    marketplace,
    network,
    pages,
    payments,
    tasks,
    wheel,
)

app = FastAPI(title="TriBoost", version="1.0.0")

app.include_router(pages.router, tags=["Pages"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(history.router, prefix="/api/history", tags=["History"])
app.include_router(formations.router, prefix="/api/formations", tags=["Formations"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(affaires.router, prefix="/api/affaires", tags=["Affaires"])
app.include_router(boost.router, prefix="/api/boost", tags=["Boost"])
app.include_router(wheel.router, prefix="/api/wheel", tags=["Wheel"])