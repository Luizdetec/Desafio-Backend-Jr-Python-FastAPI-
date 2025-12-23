from pydantic import BaseModel
from typing import Any, Optional

class GenericResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[dict] = None

class GameOutput(BaseModel):
    id: str
    name: str
    console_name: str
    console_id: str

    class Config:
        from_attributes = True