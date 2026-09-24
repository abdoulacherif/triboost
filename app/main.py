from fastapi import FastAPI

from app.routes import auth, formations, history, marketplace, network, pages, payments

app = FastAPI(title="TriBoost", version="1.0.0")

# Pages HTML
app.include_router(pages.router, tags=["Pages"])

# API
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(history.router, prefix="/api/history", tags=["History"])
app.include_router(formations.router, prefix="/api/formations", tags=["Formations"])


# ⚠️ ROUTE TEMPORAIRE DE DEBUG — À SUPPRIMER APRÈS
@app.get("/debug/routes")
async def debug_routes():
    routes = []
    for r in app.routes:
        if hasattr(r, "path") and hasattr(r, "methods"):
            routes.append({
                "path": r.path,
                "methods": list(r.methods),
                "endpoint": r.endpoint.__name__ if hasattr(r, "endpoint") else "?",
            })
    return {"total": len(routes), "routes": routes}