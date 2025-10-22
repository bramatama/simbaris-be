from app.config.supabase import supabase
from app.domain.user import User
import bcrypt

class AuthRepository:
    
    @staticmethod
    def login_team_leader(unique_team_code: str, password: str):
        # Cari tim berdasarkan unique_team_code
        team_resp = supabase.table("teams").select("created_by").eq("unique_team_code", unique_team_code).execute()
        if not team_resp.data:
            return None
        user_id = team_resp.data[0]["created_by"]
        # Ambil user dari tabel users
        user_resp = supabase.table("users").select("*").eq("user_id", user_id).execute()
        if not user_resp.data:
            return None
        user_data = user_resp.data[0]
        email = user_data["email"]
        # Login ke Supabase Auth menggunakan email dan password
        auth_resp = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if not auth_resp.user or not auth_resp.session:
            return None
        access_token = auth_resp.session.access_token
        refresh_token = auth_resp.session.refresh_token
        return {
            "user": User(**user_data),
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def register_team_leader(email: str, password: str) -> User:
        # Register ke Supabase Auth
        auth_response = supabase.auth.sign_up({"email": email, "password": password})
        user_id = auth_response.user.id if auth_response.user else None
        # Hash password sebelum simpan ke tabel users
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        data = {
            "user_id": user_id,
            "role": "team_leader",
            "email": email,
            "password": hashed_pw
            # created_at otomatis dari Supabase
        }
        db_response = supabase.table("users").insert(data).execute()
        # created_at dan field lain diambil dari response Supabase
        user_data = db_response.data[0] if db_response.data else data
        return User(**user_data)