from app.config.supabase import supabase
from typing import List, Dict, Any, Optional


class TeamRepository:
	@staticmethod
	def get_teams_summary(limit: int = 20) -> List[Dict[str, Any]]:

		response = (
			supabase.table("teams")
			.select("team_id,team_name,team_logo_url,schools(school_name),members(member_id)")
			.limit(limit)
			.execute()
		)
		items = response.data or []

		results: List[Dict[str, Any]] = []
		for it in items:
			school_name = None
			if isinstance(it.get("schools"), list) and len(it.get("schools")) > 0:
				school_name = it.get("schools")[0].get("school_name")
			elif isinstance(it.get("schools"), dict):
				school_name = it.get("schools").get("school_name")

			members = it.get("members") or []
			member_count = len(members) if isinstance(members, list) else 0

			results.append(
				{
					"team_id": it.get("team_id"),
					"team_name": it.get("team_name"),
					"team_logo_url": it.get("team_logo_url"),
					"school_name": school_name,
					"member_count": member_count,
				}
			)

		return results

	@staticmethod
	def get_team_full(team_id: str) -> Optional[Dict[str, Any]]:
		response = (
			supabase.table("teams")
			.select("*,schools(*),members(*)")
			.eq("team_id", team_id)
			.maybe_single()
			.execute()
		)
		return response.data

	@staticmethod
	def update_team(team_id: str, data: Dict[str, Any]) -> Dict[str, Any]:

		response = (
			supabase.table("teams")
			.update(data)
			.eq("team_id", team_id)
			.execute()
		)
		if not response.data:
			raise HTTPException(status_code=404, detail="Team not found or failed to update")
		return response.data[0]

