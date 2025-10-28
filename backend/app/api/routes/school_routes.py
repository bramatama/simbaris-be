from fastapi import APIRouter, status
from app.services.school_service import SchoolService
from app.domain.school import School, SchoolCreate
from typing import List

router = APIRouter(prefix="/schools", tags=["Schools"])

@router.get("/", response_model=List[School])
def get_schools(limit: int = 20):
    return SchoolService.get_schools(limit=limit)
    
@router.get("/{school_id}", response_model=School)
def get_school_detail(school_id: str):
    return SchoolService.get_school_detail(school_id)

@router.post("/", response_model=School, status_code=201)
async def create_school(school_data: SchoolCreate):
    return SchoolService.create_school(school_data.dict())