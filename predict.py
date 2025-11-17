import pickle
from fastapi import FastAPI
from pydantic import BaseModel, Field


# Input / output models
from pydantic import BaseModel, Field

class Match(BaseModel):
    first_blood: int = Field(..., ge=0, le=1)
    first_turret: int = Field(..., ge=0, le=1)
    first_dragon: int = Field(..., ge=0, le=1)
    wards_placed: int = Field(..., ge=0)
    wards_destroyed: int = Field(..., ge=0)
    kills_diff: int
    deaths_diff: int
    assists_diff: int
    dragons_diff: int
    heralds_diff: int = Field(..., ge=-1, le=1)
    voidgrubs_diff: int = Field(..., ge=-6, le=6)
    towers_diff: int = Field(..., ge=-11, le=11)
    plates_diff: int = Field(..., ge=-15, le=15)
    gold_diff: int
    cs_diff: int


class PredictResponse(BaseModel):
    win_probability: float
    win: bool


# Load trained pipeline
app = FastAPI(title="league-match-prediction")

with open("model.bin", "rb") as f_in:
    pipeline = pickle.load(f_in)


# Prediction helper
def predict_single(match: Match):
    X = [match.model_dump()]  # already numeric features in the correct order
    prob = pipeline.predict_proba(X)[0, 1]
    return float(prob)


# API endpoint
@app.post("/predict")
def predict(match: Match) -> PredictResponse:
    prob = predict_single(match)
    return PredictResponse(win_probability=prob, win=prob >= 0.5)


# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9696)