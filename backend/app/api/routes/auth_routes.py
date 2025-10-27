from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from app.services.auth_service import AuthService
from app.domain.user import UserLogin, Token, UserCreate

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, auth_service: AuthService = Depends(AuthService)):
    return auth_service.login(user_login)

@router.post("/register/team-leader", status_code=status.HTTP_201_CREATED)
def register_team_leader(user_create: UserCreate, auth_service: AuthService = Depends(AuthService)):
    return auth_service.register_team_leader(user_create)

@router.post("/logout")
async def logout(token: str = Depends(security), auth_service: AuthService = Depends(AuthService)):
    return auth_service.logout(token.credentials)

