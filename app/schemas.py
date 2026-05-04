from pydantic import BaseModel, Field
from datetime import datetime


class QueueJoinRequest(BaseModel):
    player_id: str = Field(min_length=1, max_length=64)
    role: str
    mmr: int = Field(ge=0, le=5000)


class QueuedPlayerResponse(BaseModel):
    player_id: str
    role: str
    mmr: int


class QueueListResponse(BaseModel):
    hunters: list[QueuedPlayerResponse]
    monsters: list[QueuedPlayerResponse]


class QueueLeaveRequest(BaseModel):
    player_id: str = Field(min_length=1, max_length=64)

class QueueLeaveResponse(BaseModel):
    player_id: str
    removed: bool


class MatchResponse(BaseModel):
    match_id: int
    monster: str
    hunters: list[str]
    average_mmr: int

class MatchmakingRunResponse(BaseModel):
    match_created: bool
    match: MatchResponse | None = None
    detail: str

    # Debug info (optional)
    monster_mmr: int | None = None
    allowed_min_mmr: int | None = None
    allowed_max_mmr: int | None = None
    eligible_hunters: int | None = None

class ClearQueueResponse(BaseModel):
    removed_players: int
    detail: str

class MatchHistoryResponse(BaseModel):
    match_id: int
    monster: str
    hunters: list[str]
    average_mmr: int
    created_at: datetime