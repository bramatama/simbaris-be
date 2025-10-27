from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.auth_service import AuthService
from app.domain.user import UserLogin, Token, UserCreate

templates = Jinja2Templates(directory="app/templates")

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

@router.post("/reset-password")
async def request_reset_password(
    token: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(AuthService)
):

    return auth_service.request_reset_password(token.credentials)

@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(
    request: Request,
    access_token: str = None,
    refresh_token: str = None,
    type: str = None
):

    # Tampilkan form reset password
    return templates.TemplateResponse(
        "reset_password.html", 
        {
            "request": request,
            "title": "Reset Password",
            "access_token": access_token,
            "type": type
        }
    )

@router.post("/update-password")
async def update_password(
    password_update: dict,
    token: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(AuthService)
):
    if not password_update.get("new_password"):
        raise HTTPException(status_code=400, detail="New password is required")
    return auth_service.update_password(token.credentials, password_update["new_password"])

