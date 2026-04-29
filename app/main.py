from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, wait_for_database, get_db
from app.models import QueuedPlayer
from app.schemas import QueuedPlayerResponse, QueueJoinRequest


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