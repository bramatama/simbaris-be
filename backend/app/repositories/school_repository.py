from app.config.supabase import supabase
from app.domain.school import School

class SchoolRepository:
    @staticmethod
    def get_all_schools(limit: int = 20):

        response = supabase.table("schools").select("*").limit(limit).execute()
        schools_data = response.data or []
        return [School(**school) for school in schools_data]
        
    @staticmethod
    def get_school_by_id(school_id: str):

        response = supabase.table("schools").select("*").eq("school_id", school_id).execute()
        if not response.data:
            return None
        return School(**response.data[0])
        
    @staticmethod
    def check_school_exists(school_name: str, city: str = None) -> bool:

        query = supabase.table("schools").select("*").ilike("school_name", school_name)
        if city:
            query = query.eq("city", city)
        
        response = query.execute()
        return len(response.data) > 0
        
    @staticmethod
    def create_school(school: School) -> School:

        school_data = {
            "school_id": str(school.school_id),
            "school_name": school.school_name,
            "level": school.level,
            "province": school.province,
            "city": school.city,
            "subdistrict": school.subdistrict,
            "created_at": school.created_at.isoformat()
        }
        
        response = supabase.table("schools").insert(school_data).execute()
        if not response.data:
            return None
        return School(**response.data[0])
