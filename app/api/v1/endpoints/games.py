from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.api.deps import get_current_user, RoleChecker
from app.infrastructure.database.session import get_db
from app.api.response_handler import success_response, error_response
from app.application.schemas.game_schemas import GameCreate, GameOutput
from app.infrastructure.repositories.sqlalchemy_game_repository import SQLAlchemyGameRepository
from app.infrastructure.repositories.sqlalchemy_console_repository import SQLAlchemyConsoleRepository
from app.domain.entities.game import Game

router = APIRouter()

@router.post("/", dependencies=[Depends(RoleChecker(["admin"]))])
async def create_game(
        game_in: GameCreate,
        db: AsyncSession = Depends(get_db)
):
    game_repo = SQLAlchemyGameRepository(db)
    console_repo = SQLAlchemyConsoleRepository(db)

    console = await console_repo.find_by_id(game_in.console_id)
    if not console:
        return error_response(
            message="The specified console does not exist",
            code="NOT_FOUND"
        )

    new_game = Game(
        id=uuid.uuid4(),
        name=game_in.name,
        console_id=game_in.console_id,
        console_name=console.name
    )

    await game_repo.save(new_game)

    return success_response(data={
        "id": str(new_game.id),
        "name": new_game.name,
        "console_name": new_game.console_name,
        "console_id": str(new_game.console_id)
    })


@router.get("/")
async def list_games(
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    game_repo = SQLAlchemyGameRepository(db)
    games = await game_repo.list_all()

    results = [
        {
            "id": str(g.id),
            "name": g.name,
            "console_name": g.console.name,
            "console_id": str(g.console_id)
        } for g in games
    ]
    return success_response(data=results)


@router.get("/consoles/{console_id}/games")
async def list_games_by_console(
        console_id: str,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    game_repo = SQLAlchemyGameRepository(db)
    games = await game_repo.list_by_console(console_id)

    results = [
        {
            "id": str(g.id),
            "name": g.name,
            "console_name": g.console.name,
            "console_id": str(g.console_id)
        } for g in games
    ]
    return success_response(data=results)