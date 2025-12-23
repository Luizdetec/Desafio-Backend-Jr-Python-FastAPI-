from pydantic import BaseModel, ConfigDict
from uuid import UUID

class ConsoleBase(BaseModel):
    name: str
    company: str

class ConsoleCreate(ConsoleBase):
    pass

class ConsoleOutput(ConsoleBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)