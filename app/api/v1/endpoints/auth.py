from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.application.services.auth_service import AuthService
from app.application.schemas.auth_schemas import UserCreate
from app.api.response_handler import success_response, error_response

router = APIRouter()


@router.post("/register")
async def register(
        user_in: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    user_repo = SQLAlchemyUserRepository(db)
    auth_service = AuthService(user_repo)

    try:
        new_user = await auth_service.register_user(user_in)

        return success_response(data={
            "id": str(new_user.id),
            "username": new_user.username,
            "role": new_user.role  # admin ou user
        })
    except Exception as e:
        return error_response(message=str(e), code="BAD_REQUEST")


@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    user_repo = SQLAlchemyUserRepository(db)
    auth_service = AuthService(user_repo)

    # O AuthService valida as credenciais e gera o token com expiração de 1 hora [cite: 89]
    token = await auth_service.authenticate(form_data.username, form_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response("Invalid username or password", "UNAUTHORIZED")
        )

    return success_response(data={
        "access_token": token,
        "token_type": "bearer"
    })