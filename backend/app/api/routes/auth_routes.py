from fastapi import APIRouter, HTTPException
from app.services.auth_service import AuthService
from app.domain.user import User
from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    unique_team_code: str
    password: str

class LoginResponse(BaseModel):
    user: User
    access_token: str
    refresh_token: str

router = APIRouter()

@router.post("/register/team-leader", response_model=User)
def register_team_leader(req: RegisterRequest):
    if not req.email or not req.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    user = AuthService.register_team_leader(req.email, req.password)
    # Hapus password dari response
    if hasattr(user, "dict"):
        user = user.dict()
    user.pop("password", None)
    return user


@router.post("/login/team-leader", response_model=LoginResponse)
def login_team_leader(req: LoginRequest):
    result = AuthService.login_team_leader(req.unique_team_code, req.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid team code or password")
    user = result["user"]
    if hasattr(user, "dict"):
        user = user.dict()

    user.pop("password", None)
    return LoginResponse(
        user=user,
        access_token=result["access_token"],
        refresh_token=result["refresh_token"]
    )
