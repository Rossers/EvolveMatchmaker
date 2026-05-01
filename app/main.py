from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, wait_for_database, get_db
from app.models import QueuedPlayer
from app.schemas import (
    QueuedPlayerResponse,
    QueueJoinRequest,
    QueueListResponse,
    QueueLeaveRequest,
    QueueLeaveResponse,
)


app = FastAPI(title="Evolve Matchmaker API")


@app.on_event("startup")
def startup_event():
    wait_for_database()
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/queue/join", response_model=QueuedPlayerResponse)
def join_queue(request: QueueJoinRequest, db: Session = Depends(get_db)):
    if request.role not in ["hunter", "monster"]:
        raise HTTPException(
            status_code=400,
            detail="role must be either 'hunter' or 'monster'",
        )

    existing_player = (
        db.query(QueuedPlayer)
        .filter(QueuedPlayer.player_id == request.player_id)
        .first()
    )

    if existing_player:
        raise HTTPException(
            status_code=409,
            detail="player is already queued",
        )

    queued_player = QueuedPlayer(
        player_id=request.player_id,
        role=request.role,
        mmr=request.mmr,
    )

    db.add(queued_player)
    db.commit()
    db.refresh(queued_player)

    return queued_player


@app.get("/queue", response_model=QueueListResponse)
def get_queue(db: Session = Depends(get_db)):
    queued_players = db.query(QueuedPlayer).order_by(QueuedPlayer.joined_at).all()

    hunters = []
    monsters = []

    for player in queued_players:
        response_player = QueuedPlayerResponse(
            player_id=player.player_id,
            role=player.role,
            mmr=player.mmr,
        )

        if player.role == "hunter":
            hunters.append(response_player)
        elif player.role == "monster":
            monsters.append(response_player)

    return QueueListResponse(
        hunters=hunters,
        monsters=monsters,
    )

@app.post("/queue/leave", response_model=QueueLeaveResponse)
def leave_queue(request: QueueLeaveRequest, db: Session = Depends(get_db)):
    queued_player = (
        db.query(QueuedPlayer)
        .filter(QueuedPlayer.player_id == request.player_id)
        .first()
    )

    if not queued_player:
        raise HTTPException(
            status_code=404,
            detail="player is not currently queued",
        )

    db.delete(queued_player)
    db.commit()

    return QueueLeaveResponse(
        player_id=request.player_id,
        removed=True,
    )