from fastapi import FastAPI

from app.routes import (
    admin,
    admin_content,
    admin_courses,
    admin_shop,
    ads,
    affaires,
    auth,
    boost,
    chat,
    courses,
    formations,
    history,
    lesson_api,
    marketplace,
    network,
    pages,
    payments,
    shop,
    tasks,
    wheel,
)

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
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(affaires.router, prefix="/api/affaires", tags=["Affaires"])
app.include_router(boost.router, prefix="/api/boost", tags=["Boost"])
app.include_router(wheel.router, prefix="/api/wheel", tags=["Wheel"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(admin_content.router, prefix="/api/admin/content", tags=["AdminContent"])
app.include_router(admin_shop.router, prefix="/api/admin/shop", tags=["AdminShop"])
app.include_router(admin_courses.router, prefix="/api/admin/courses", tags=["AdminCourses"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(shop.router, prefix="/api/shop", tags=["Shop"])
app.include_router(ads.router, prefix="/api/ads", tags=["Ads"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(lesson_api.router, prefix="/api/lesson", tags=["LessonAPI"])