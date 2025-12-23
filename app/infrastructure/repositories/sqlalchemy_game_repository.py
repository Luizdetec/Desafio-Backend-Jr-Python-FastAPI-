from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.infrastructure.database.models import GameModel, ConsoleModel
from app.domain.entities.game import Game
from typing import List, Any, Coroutine, Sequence
import uuid


class SQLAlchemyGameRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, game: Game) -> Game:
        new_game = GameModel(id=game.id, name=game.name, console_id=game.console_id)
        self.session.add(new_game)
        await self.session.commit()
        return game

    async def list_all(self) -> Sequence[GameModel]:
        result = await self.session.execute(
            select(GameModel).options(joinedload(GameModel.console))
        )
        return result.scalars().all()

    async def list_by_console(self, console_id: str) -> Sequence[GameModel]:
        try:
            console_uuid = uuid.UUID(console_id) if isinstance(console_id, str) else console_id
        except (ValueError, AttributeError):
            return []

        result = await self.session.execute(
            select(GameModel)
            .where(GameModel.console_id == console_uuid)
            .options(joinedload(GameModel.console))
        )
        return result.scalars().all()