from fastapi import APIRouter
from src.interface.http.version1.routes.auth_route import router as v1_auth_router
# from src.interface.http.version1.routes.budget_route import router as v1_budget_router
# from src.interface.http.version1.routes.categories_route import router as v1_categories_router
# from src.interface.http.version1.routes.notification_route import router as v1_notification_router
# from src.interface.http.version1.routes.transactions_route import router as v1_transactions_router
# from src.interface.http.version1.routes.users_route import router as v1_users_router



api_router = APIRouter()

# Đăng ký router cho từng module, từng version
api_router.include_router(v1_auth_router, prefix="/api/v1")
# api_router.include_router(v1_budget_router, prefix="/api/v1")
# api_router.include_router(v1_categories_router, prefix="/api/v1")
# api_router.include_router(v1_notification_router, prefix="/api/v1")
# api_router.include_router(v1_transactions_router, prefix="/api/v1")
# api_router.include_router(v1_users_router, prefix="/api/v1")


# Trong main.py:
# from interface.routes import api_router
# app.include_router(api_router)