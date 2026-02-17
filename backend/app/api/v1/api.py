from fastapi import APIRouter
from app.api.v1.endpoints import auth, admin, technicians, customers

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(technicians.router, prefix="/technician", tags=["technician"])
api_router.include_router(customers.router, prefix="/customer", tags=["customer"])
