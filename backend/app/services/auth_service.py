from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository
from app.domain.user import UserLogin, Token, UserCreate
from fastapi import HTTPException

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()
        self.user_repository = UserRepository()

    def login(self, user_login: UserLogin) -> Token:
        try:
            response = self.auth_repository.login(user_login)
            if response.session and response.session.access_token:
                return Token(access_token=response.session.access_token, token_type="bearer")
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    def logout(self, token: str):
        try:
            self.auth_repository.logout(token)
            return {"message": "Successfully logged out"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def register_team_leader(self, user_create: UserCreate):
        try:
            auth_response = self.auth_repository.sign_up(user_create)
            
            if not auth_response.user or not auth_response.user.id:
                raise HTTPException(status_code=400, detail="Failed to create user in authentication service")

            user_id = auth_response.user.id

            profile = self.user_repository.create_user_profile(user_id, user_create)
            
            if not profile:

                raise HTTPException(status_code=500, detail="Failed to create user profile in database")

            return profile

        except HTTPException as e:
            raise e
        except Exception as e:

            if "User already registered" in str(e):
                raise HTTPException(status_code=409, detail="User with this email already exists")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
        
    def request_reset_password(self, token: str):
        try:
            self.auth_repository.request_reset_password(token)
            return {"message": "Password reset link has been sent to your email"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_password(self, token: str, new_password: str):
        try:
            self.auth_repository.update_password(token, new_password)
            return {"message": "Password has been updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def logout(self, token: str):
        try:
            self.auth_repository.logout(token)
            return {"message": "Successfully logged out"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))