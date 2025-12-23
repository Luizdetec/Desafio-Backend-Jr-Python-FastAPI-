from fastapi import APIRouter
from app.api.v1.endpoints import auth, consoles, games

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(consoles.router, prefix="/consoles", tags=["consoles"])
api_router.include_router(games.router, prefix="/games", tags=["games"])