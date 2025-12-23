import uuid
from typing import Optional

from app.application.schemas.auth_schemas import UserCreate
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_handler import PasswordHandler
from app.infrastructure.security.jwt_handler import create_access_token


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> User:
        existing_user = await self.user_repo.find_by_username(user_data.username)
        if existing_user:
            raise Exception("User already exists")

        new_user = User(
            id=uuid.uuid4(),
            username=user_data.username,
            password_hash=PasswordHandler.hash_password(user_data.password),  #
            role=user_data.role  # Define se é admin ou user
        )

        return await self.user_repo.save(new_user)

    async def authenticate(self, username: str, password: str) -> Optional[str]:
        user = await self.user_repo.find_by_username(username)

        if not user or not PasswordHandler.verify_password(password, user.password_hash):
            return None

        token_data = {
            "sub": user.username,
            "role": user.role
        }

        return create_access_token(token_data)