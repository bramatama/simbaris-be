from pydantic import BaseModel, EmailStr
from uuid import UUID

class User(BaseModel):
    user_id: UUID
    email: str
    role: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
