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

    def request_reset_password(self, token: str):

        try:
            # Set session untuk mendapatkan user yang sedang login
            current_session = supabase.auth.get_session()
            if not current_session or not current_session.user:
                raise HTTPException(status_code=401, detail="No active session")
            
            # Ambil email dari session
            email = current_session.user.email
            if not email:
                raise HTTPException(status_code=400, detail="User email not found")
                
            # Kirim email reset password dengan redirect URL 
            return supabase.auth.reset_password_email(
                email,
                options={
                    "redirect_to": "http://localhost:8000/api/auth/reset-password"
                }
            )
        except Exception as e:
            raise e
            
    def update_password(self, token: str, new_password: str):

        try:
            # Update password menggunakan token recovery
            response = supabase.auth.update_user({
                "password": new_password
            })
            return response
        except Exception as e:
            raise e


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = supabase.auth.get_user(token)
        user_id = payload.user.id
        
        user_repo = UserRepository()
        user = user_repo.get_user_by_id(user_id)

        print(f"Authenticated user ID: {user}")
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found in database")
            
        return user
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
