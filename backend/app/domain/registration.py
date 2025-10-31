from pydantic import BaseModel, Field
from typing import Optional, List 
from datetime import datetime
from uuid import UUID, uuid4
from .team import LoadRegistration

class Registration(BaseModel):
    registration_id: UUID = Field(default_factory=uuid4)
    team_id: Optional[UUID] = None
    status: str = 'pending'
    price: Optional[float] = None
    payment_proof: Optional[str] = None
    verified_by: Optional[UUID] = None
    verification_message: Optional[str] = None
    verified_at: Optional[datetime] = None
    submitted_at: datetime = Field(default_factory=datetime.now)
    last_update: datetime = Field(default_factory=datetime.now)

    teams: Optional[LoadRegistration] = None

    class Config:
        orm_mode = True

class RegistrationCreate(BaseModel):
    team_id: UUID
    price: float

class RegistrationUpdate(BaseModel):
    status: Optional[str] = None
    payment_proof: Optional[str] = None
    verification_message: Optional[str] = None