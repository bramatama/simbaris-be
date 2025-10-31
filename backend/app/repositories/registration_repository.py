from app.config.supabase import supabase
from app.domain.registration import Registration, RegistrationCreate, RegistrationUpdate
from typing import List, Optional
from uuid import UUID

class RegistrationRepository:
    def get_all(self, status: Optional[str] = None) -> List[Registration]:
        query = supabase.table("registration").select("*")
        
        if status:
            query = query.eq("status", status)
            
        response = query.execute()
        return [Registration(**data) for data in response.data]

    def get_by_id(self, registration_id: UUID) -> Optional[Registration]:
        response = supabase.table("registration").select("*, teams(*)").eq("registration_id", str(registration_id)).execute()
        if not response.data:
            return None
        return Registration(**response.data[0])

    def create(self, registration: RegistrationCreate) -> Registration:
        response = supabase.table("registration").insert(registration.dict()).execute()
        return Registration(**response.data[0])

    def update(self, registration_id: UUID, registration: RegistrationUpdate) -> Optional[Registration]:
        response = supabase.table("registration").update(registration.dict(exclude_unset=True)).eq("registration_id", str(registration_id)).execute()
        if not response.data:
            return None
        return Registration(**response.data[0])
