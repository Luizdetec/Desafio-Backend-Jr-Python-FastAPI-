from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models import UserModel
from app.domain.entities.user import User

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        db_user = UserModel(
            id=user.id,
            username=user.username,
            password_hash=user.password_hash,
            role=user.role
        )
        self.session.add(db_user)
        await self.session.commit()
        return user

    async def find_by_username(self, username: str):
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user_model = result.scalars().first()
        if user_model:
            return User(
                id=user_model.id,
                username=user_model.username,
                password_hash=user_model.password_hash,
                role=user_model.role
            )
        return None