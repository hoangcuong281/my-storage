from fastapi import FastAPI
from routers import (
    product_router,
    category_router,
    supplier_router,
    stock_router,
    auth_router,
    user_router,
)
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Warehouse Management API")

app.add_middleware(
    SessionMiddleware,
    secret_key="SESSION_SECRET_KEY_123456",  # đổi key này
    session_cookie="session",
    max_age=60 * 60,  # 1 giờ
    same_site="lax",
    https_only=False  # True nếu dùng HTTPS
)
app.include_router(category_router.router)
app.include_router(supplier_router.router)
app.include_router(product_router.router)
app.include_router(stock_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)

