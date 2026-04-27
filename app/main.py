from fastapi import FastAPI

app = FastAPI(title="Hunter Matchmaking API")


@app.get("/health")
def health_check():
    return {"status": "ok"}