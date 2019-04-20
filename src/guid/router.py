"""Router for gathering the views together."""
from fastapi import APIRouter
from guid import views


api_router = APIRouter()
api_router.include_router(views.router, prefix="/guid", tags=["guid"])
