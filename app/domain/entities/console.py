from dataclasses import dataclass
from uuid import UUID


@dataclass
class Console:
    id: UUID
    name: str
    company: str