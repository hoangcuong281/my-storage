from fastapi import FastAPI
from routers import (
    product_router,
    category_router,
    supplier_router,
    stock_router,
)

app = FastAPI(title="Warehouse Management API")

app.include_router(category_router.router)
app.include_router(supplier_router.router)
app.include_router(product_router.router)
app.include_router(stock_router.router)

