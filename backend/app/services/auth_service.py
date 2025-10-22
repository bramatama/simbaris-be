from app.repositories.auth_repository import AuthRepository
from app.domain.user import User
from typing import Optional

class AuthService:
    @staticmethod
    def login_team_leader(unique_team_code: str, password: str):
        return AuthRepository.login_team_leader(unique_team_code, password)
    
    def register_team_leader(email: str, password: str) -> User:
        return AuthRepository.register_team_leader(email, password)

