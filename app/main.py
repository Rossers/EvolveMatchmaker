from fastapi import FastAPI

from app.database import Base, engine, wait_for_database
from app import models

app = FastAPI(title="Evolve Matchmaker API")


@app.on_event("startup")
def startup_event():
    wait_for_database()
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}