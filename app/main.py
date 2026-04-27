from fastapi import FastAPI

app = FastAPI(title="Evolve Matchmaker API")


@app.get("/health")
def health_check():
    return {"status": "ok"}