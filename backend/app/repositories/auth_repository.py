from app.config.supabase import supabase
from app.domain.user import UserLogin, UserCreate
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.repositories.user_repository import UserRepository

security = HTTPBearer()

class AuthRepository:
    def login(self, user_login: UserLogin):
        try:
            response = supabase.auth.sign_in_with_password({
                "email": user_login.email,
                "password": user_login.password
            })
            return response
        except Exception as e:
            raise e

    def sign_up(self, user_create: UserCreate):
        try:
            response = supabase.auth.sign_up({
                "email": user_create.email,
                "password": user_create.password
            })
            return response
        except Exception as e:
            raise e

    def logout(self, token: str):
        try:
            current_session = supabase.auth.get_session()
            if not current_session:
                raise HTTPException(status_code=401, detail="No active session")
            
            return supabase.auth.sign_out()
        except Exception as e:
            raise e


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = supabase.auth.get_user(token)
        user_id = payload.user.id
        
        user_repo = UserRepository()
        user = user_repo.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found in database")
            
        return user
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
