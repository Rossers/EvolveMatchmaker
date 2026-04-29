from pydantic import BaseModel, Field


class QueueJoinRequest(BaseModel):
    player_id: str = Field(min_length=1, max_length=64)
    role: str
    mmr: int = Field(ge=0, le=5000)


class QueuedPlayerResponse(BaseModel):
    player_id: str
    role: str
    mmr: int