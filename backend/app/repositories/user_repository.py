from app.config.supabase import supabase
from app.domain.user import UserCreate
from typing import Optional, Dict, Any

class UserRepository:
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:

            response = supabase.table("users").select("*, members(teams(*)), teams!created_by(*)").eq("user_id", user_id).maybe_single().execute()
            
            if response.data:
                user_data = response.data
                user_data["team"] = None

                admin_teams_list = user_data.get("teams", [])
                if admin_teams_list:
                    user_data["team"] = admin_teams_list[0]

                members_list = user_data.get("members", [])
                if not user_data["team"] and members_list and members_list[0].get("teams"):
                    user_data["team"] = members_list[0]["teams"]
                
                if "members" in user_data:
                    del user_data["members"]
                if "teams" in user_data:
                    del user_data["teams"]

                return user_data
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
