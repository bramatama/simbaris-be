from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime
from uuid import uuid4


class TeamSummary(BaseModel):
    team_id: str
    team_name: str
    team_logo_url: Optional[str] = None
    school_name: Optional[str] = None
    member_count: int = 0


class TeamDetail(BaseModel):
    # full detail - flexible shape, keep as Any for nested objects
    team_id: str
    team_name: str
    coach_name: Optional[str] = None
    supervisor_name: Optional[str] = None
    contact: Optional[str] = None
    team_logo_url: Optional[str] = None
    raw_photo_url: Optional[str] = None
    school_id: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    school: Optional[Any] = None
    members: Optional[List[Any]] = []
    registration: Optional[Any] = None


class TeamCreate(BaseModel):
    name: str
    members: Optional[List[str]] = []


class TeamUpdate(BaseModel):
    coach_name: Optional[str] = None
    supervisor_name: Optional[str] = None
    contact: Optional[str] = None
    # Some clients may send an `email` field for contact; we'll accept it and map to `contact` on update
    email: Optional[str] = None
