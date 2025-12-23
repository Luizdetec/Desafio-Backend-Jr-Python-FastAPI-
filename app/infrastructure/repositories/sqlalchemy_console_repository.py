from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.repositories.console_repository import ConsoleRepository
from app.infrastructure.database.models import ConsoleModel
from app.domain.entities.console import Console

class SQLAlchemyConsoleRepository(ConsoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, console: Console) -> Console:
        new_console = ConsoleModel(
            id=console.id,
            name=console.name,
            company=console.company
        )
        self.session.add(new_console)
        await self.session.commit()
        return console

    async def find_by_name(self, name: str):
        result = await self.session.execute(
            select(ConsoleModel).where(ConsoleModel.name == name)
        )
        return result.scalars().first()