from fastapi import APIRouter, Depends, HTTPException
from app.services.registration_service import RegistrationService
from app.domain.registration import Registration, RegistrationCreate, RegistrationUpdate
from typing import List, Optional
from uuid import UUID
from app.repositories.auth_repository import get_current_user
from app.api.deps import require_roles

router = APIRouter(prefix="/registrations", tags=["Registrations"])

@router.get("/", response_model=List[Registration], dependencies=[Depends(require_roles("committee"))])
def get_all_registrations(status: Optional[str] = None, registration_service: RegistrationService = Depends()):
    return registration_service.get_all_registrations(status=status)

@router.get("/{registration_id}", response_model=Registration, dependencies=[Depends(get_current_user)])
def get_registration_by_id(registration_id: UUID, registration_service: RegistrationService = Depends()):
    registration = registration_service.get_registration_by_id(registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    return registration

# @router.post("/", response_model=Registration, dependencies=[Depends(require_roles("team_admin"))])
# def create_registration(registration: RegistrationCreate):
#     return registration_service.create_registration(registration)

# @router.put("/{registration_id}", response_model=Registration, dependencies=[Depends(require_roles("committee"))])
# def update_registration(registration_id: UUID, registration: RegistrationUpdate):
#     updated_registration = registration_service.update_registration(registration_id, registration)
#     if not updated_registration:
#         raise HTTPException(status_code=404, detail="Registration not found")
#     return updated_registration
