from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.console import Console

class ConsoleRepository(ABC):
    @abstractmethod
    async def save(self, console: Console) -> Console:
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Console]:
        pass

    @abstractmethod
    async def list_all(self) -> List[Console]:
        pass