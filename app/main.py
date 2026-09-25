from fastapi import FastAPI

from app.routes import (
    admin,
    admin_content,
    affaires,
    auth,
    boost,
    chat,
    formations,
    history,
    marketplace,
    network,
    pages,
    payments,
    shop,
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
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(admin_content.router, prefix="/api/admin/content", tags=["AdminContent"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(shop.router, prefix="/api/shop", tags=["Shop"])