from app.repositories.school_repository import SchoolRepository
from app.domain.school import School
from typing import List

class SchoolService:
    @staticmethod
    def get_schools() -> List[School]:
        return SchoolRepository.get_all_schools()
