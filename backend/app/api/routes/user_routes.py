from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import UserService
from app.repositories.auth_repository import get_current_user

router = APIRouter()

@router.get("/me", response_model=dict)
def get_user_me(current_user: dict = Depends(get_current_user)):
    
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user
