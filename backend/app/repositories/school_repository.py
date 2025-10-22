from app.config.supabase import supabase
from app.domain.school import School

class SchoolRepository:
    @staticmethod
    def get_all_schools():
        response = supabase.table("schools").select("*").execute()
        schools_data = response.data or []
        return [School(**school) for school in schools_data]
