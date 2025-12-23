from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    password: str = Field(..., max_length=72)
    role: str = "user"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"