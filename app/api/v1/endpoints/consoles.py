from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.api.deps import get_current_user, RoleChecker
from app.infrastructure.database.session import get_db
from app.api.response_handler import success_response, error_response
from app.application.schemas.console_schemas import ConsoleCreate
from app.infrastructure.repositories.sqlalchemy_console_repository import SQLAlchemyConsoleRepository
from app.domain.entities.console import Console
from app.infrastructure.repositories.sqlalchemy_game_repository import SQLAlchemyGameRepository

router = APIRouter()


@router.post("/", dependencies=[Depends(RoleChecker(["admin"]))])
async def create_console(
        console_in: ConsoleCreate,
        db: AsyncSession = Depends(get_db)
):
    repo = SQLAlchemyConsoleRepository(db)

    existing = await repo.find_by_name(console_in.name)
    if existing:
        return error_response(
            message="A console with this name already exists",
            code="BAD_REQUEST"
        )

    new_console = Console(
        id=uuid.uuid4(),
        name=console_in.name,
        company=console_in.company
    )

    await repo.save(new_console)

    return success_response(data={
        "id": str(new_console.id),
        "name": new_console.name,
        "company": new_console.company
    })


@router.get("/")
async def list_consoles(
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    repo = SQLAlchemyConsoleRepository(db)
    consoles = await repo.list_all()

    results = [
        {
            "id": str(c.id),
            "name": c.name,
            "company": c.company
        } for c in consoles
    ]
    return success_response(data=results)


@router.get("/{console_id}/games")
async def list_games_by_console(
        console_id: str,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        uuid.UUID(console_id)
    except ValueError:
        return error_response(
            message="Invalid console ID format",
            code="BAD_REQUEST"
        )

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