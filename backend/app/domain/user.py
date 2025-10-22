from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None
    email: str
    password: Optional[str] = None
    created_at: Optional[str] = None
