from dataclasses import dataclass
from uuid import UUID

@dataclass
class User:
    id: UUID
    username: str
    password_hash: str
    role: str