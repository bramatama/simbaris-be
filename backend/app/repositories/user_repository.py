from app.config.supabase import supabase
from app.domain.user import UserCreate

class UserRepository:
    def get_user_by_id(self, user_id: str):
        try:
            response = supabase.table("users").select("*").eq("user_id", user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching user by id: {e}")
            return None

    def create_user_profile(self, user_id: str, user_create: UserCreate):
        try:
            response = supabase.table("users").upsert({
                "user_id": user_id,
                "email": user_create.email,
                "role": "team_admin"
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return None
