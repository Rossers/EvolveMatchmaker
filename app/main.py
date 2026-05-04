from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, wait_for_database, get_db
from app.models import QueuedPlayer, Match
from app.schemas import (
    QueuedPlayerResponse,
    QueueJoinRequest,
    QueueListResponse,
    QueueLeaveRequest,
    QueueLeaveResponse,
    MatchResponse,
    MatchmakingRunResponse,
    ClearQueueResponse,
    MatchHistoryResponse,
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


@app.post("/matchmaking/run", response_model=MatchmakingRunResponse)
def run_matchmaking(db: Session = Depends(get_db)):
    mmr_range = 300

    monster = (
        db.query(QueuedPlayer)
        .filter(QueuedPlayer.role == "monster")
        .order_by(QueuedPlayer.joined_at)
        .first()
    )

    if not monster:
        return MatchmakingRunResponse(
            match_created=False,
            match=None,
            detail="no monster queued",
        )

    hunters = (
        db.query(QueuedPlayer)
        .filter(
            QueuedPlayer.role == "hunter",
            QueuedPlayer.mmr >= monster.mmr - mmr_range,
            QueuedPlayer.mmr <= monster.mmr + mmr_range,
        )
        .order_by(QueuedPlayer.joined_at)
        .limit(4)
        .all()
    )

    eligible_hunters = len(hunters)

    if eligible_hunters < 4:
        return MatchmakingRunResponse(
            match_created=False,
            match=None,
            detail="no match found",
            monster_mmr=monster.mmr,
            allowed_min_mmr=monster.mmr - mmr_range,
            allowed_max_mmr=monster.mmr + mmr_range,
            eligible_hunters=eligible_hunters,
        )

    player_mmrs = [monster.mmr] + [hunter.mmr for hunter in hunters]
    average_mmr = round(sum(player_mmrs) / len(player_mmrs))

    hunter_ids = [hunter.player_id for hunter in hunters]

    match = Match(
        monster_id=monster.player_id,
        hunter_ids=hunter_ids,
        average_mmr=average_mmr,
    )

    db.add(match)

    for hunter in hunters:
        db.delete(hunter)

    db.delete(monster)

    db.commit()
    db.refresh(match)

    return MatchmakingRunResponse(
        match_created=True,
        match=MatchResponse(
            match_id=match.id,
            monster=match.monster_id,
            hunters=match.hunter_ids,
            average_mmr=match.average_mmr,
        ),
        detail="match created",
    )


@app.delete("/dev/queue", response_model=ClearQueueResponse)
def clear_queue(db: Session = Depends(get_db)):
    removed_players = db.query(QueuedPlayer).delete()
    db.commit()

    return ClearQueueResponse(
        removed_players=removed_players,
        detail="queue cleared",
    )


@app.get("/matches", response_model=list[MatchHistoryResponse])
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(Match).order_by(Match.created_at.desc()).all()

    return [
        MatchHistoryResponse(
            match_id=match.id,
            monster=match.monster_id,
            hunters=match.hunter_ids,
            average_mmr=match.average_mmr,
            created_at=match.created_at,
        )
        for match in matches
    ]