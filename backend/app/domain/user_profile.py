from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class TeamInProfile(BaseModel):
    team_id: UUID
    team_name: str
    # field lain kalau perlu 

class UserProfile(BaseModel):
    user_id: UUID
    email: str
    role: str
    team: Optional[TeamInProfile] = None