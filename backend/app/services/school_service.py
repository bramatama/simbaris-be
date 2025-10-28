from app.repositories.school_repository import SchoolRepository
from app.domain.school import School
from typing import List
from fastapi import HTTPException

class SchoolService:
    @staticmethod
    def get_schools(limit: int = 20) -> List[School]:
        return SchoolRepository.get_all_schools(limit=limit)
        
    @staticmethod
    def get_school_detail(school_id: str) -> School:
        school = SchoolRepository.get_school_by_id(school_id)
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        return school

    @staticmethod
    def create_school(school_data: dict) -> School:
        if SchoolRepository.check_school_exists(
            school_name=school_data["school_name"],
            city=school_data.get("city")
        ):
            raise HTTPException(
                status_code=400,
                detail="School with this name already exists in the specified city"
            )
            
        # Buat instance School baru
        new_school = School.create(
            school_name=school_data["school_name"],
            level=school_data.get("level"),
            province=school_data.get("province"),
            city=school_data.get("city"),
            subdistrict=school_data.get("subdistrict")
        )
        
        # Simpan ke database
        created_school = SchoolRepository.create_school(new_school)
        if not created_school:
            raise HTTPException(
                status_code=500,
                detail="Failed to create school"
            )
            
        return created_school