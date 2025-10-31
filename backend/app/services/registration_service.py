from app.repositories.registration_repository import RegistrationRepository
from app.domain.registration import Registration, RegistrationCreate, RegistrationUpdate
from typing import List, Optional
from uuid import UUID

class RegistrationService:
    def __init__(self):
        self.repository = RegistrationRepository()

    def get_all_registrations(self, status: Optional[str] = None) -> List[Registration]:
        return self.repository.get_all(status=status)

    def get_registration_by_id(self, registration_id: UUID) -> Optional[Registration]:
        return self.repository.get_by_id(registration_id)

    def create_registration(self, registration: RegistrationCreate) -> Registration:
        return self.repository.create(registration)

    def update_registration(self, registration_id: UUID, registration: RegistrationUpdate) -> Optional[Registration]:
        return self.repository.update(registration_id, registration)
