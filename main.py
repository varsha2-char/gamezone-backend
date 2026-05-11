from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json, os

app = FastAPI(title="GameZone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SCORES_FILE = "scores.json"

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE) as f:
            return json.load(f)
    return []

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

class ScoreEntry(BaseModel):
    name: str
    score: int
    game: str = "snake"

@app.get("/")
def root():
    return {"message": "GameZone API is running!"}

@app.get("/leaderboard", response_model=List[ScoreEntry])
def get_leaderboard(game: str = "snake"):
    scores = load_scores()
    filtered = [s for s in scores if s.get("game") == game]
    return sorted(filtered, key=lambda x: x["score"], reverse=True)[:10]

@app.post("/leaderboard")
def add_score(entry: ScoreEntry):
    scores = load_scores()
    scores.append(entry.dict())
    save_scores(scores)
    return {"message": "Score saved!", "entry": entry}
