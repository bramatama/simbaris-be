from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.services.team_service import TeamService
from app.domain.team import TeamSummary, TeamDetail, TeamUpdate
from app.repositories.auth_repository import get_current_user
from app.api.deps import require_roles

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("/", response_model=List[TeamSummary])
def list_teams(limit: int = 20, current_user=Depends(require_roles("committee", "team_admin"))):
	return TeamService.get_teams_summary(limit=limit)


@router.get("/{team_id}", response_model=TeamDetail)
def get_team(team_id: str, current_user=Depends(get_current_user)):
	return TeamService.get_team_detail(team_id)


@router.put("/{team_id}", response_model=Dict[str, Any])
def update_team(
    team_id: str,
    team_update: TeamUpdate,
    current_user=Depends(require_roles("team_admin")),
):
    return TeamService.update_team(team_id, team_update)
