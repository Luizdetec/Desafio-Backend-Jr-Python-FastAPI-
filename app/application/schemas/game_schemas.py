from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class GameBase(BaseModel):
    name: str

class GameCreate(GameBase):
    console_id: UUID

class GameOutput(GameBase):
    id: UUID
    console_id: UUID
    console_name: str

    model_config = ConfigDict(from_attributes=True)

class GameListResponse(BaseModel):
    success: bool = True
    data: list[GameOutput]