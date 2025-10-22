from fastapi import APIRouter
from app.services.school_service import SchoolService
from app.domain.school import School
from typing import List

router = APIRouter()

@router.get("/schools", response_model=List[School])
def get_schools():
    return SchoolService.get_schools()
