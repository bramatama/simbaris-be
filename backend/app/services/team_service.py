from app.repositories.team_repository import TeamRepository
from app.domain.team import TeamSummary, TeamDetail, TeamUpdate
from fastapi import HTTPException
from typing import List, Dict, Any


class TeamService:
	@staticmethod
	def get_teams_summary(limit: int = 20) -> List[TeamSummary]:
		items = TeamRepository.get_teams_summary(limit=limit)
		return [TeamSummary(**it) for it in items]

	@staticmethod
	def get_team_detail(team_id: str) -> TeamDetail:
		data = TeamRepository.get_team_full(team_id)
		if not data:
			raise HTTPException(status_code=404, detail="Team not found")
		return TeamDetail(**data)

	@staticmethod
	def update_team(team_id: str, team_update: TeamUpdate) -> Dict[str, Any]:
		update_data = team_update.dict(exclude_unset=True)

		if "email" in update_data:
			update_data["contact"] = update_data.pop("email")

		if not update_data:
			raise HTTPException(status_code=400, detail="No fields to update")

		return TeamRepository.update_team(team_id, update_data)
