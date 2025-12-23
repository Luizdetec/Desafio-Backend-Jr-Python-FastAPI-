from dataclasses import dataclass
from uuid import UUID

@dataclass
class Game:
    id: UUID
    name: str
    console_id: UUID
    console_name: str = None