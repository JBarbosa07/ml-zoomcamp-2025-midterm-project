import pickle
from typing import Literal
from pydantic import BaseModel, Field


from fastapi import FastAPI
import uvicorn


class Match(BaseModel):
    bluefirstblood: Literal[0, 1]
    bluefirstturret: Literal[0, 1]
    bluefirstdragon: Literal[0, 1]

    bluewardsplaced: int = Field(..., ge=0)
    bluecontrolwardsplaced: int = Field(..., ge=0)
    bluewardsdestroyed: int = Field(..., ge=0)
    bluecontrolwardsdestroyed: int = Field(..., ge=0)

    bluekills: int = Field(..., ge=0)
    bluedeaths: int = Field(..., ge=0)
    blueassists: int = Field(..., ge=0)

    bluedragons: int = Field(..., ge=0)
    blueheralds: int = Field(..., ge=0)
    bluevoidgrubs: int = Field(..., ge=0)

    bluetowersdestroyed: int = Field(..., ge=0)
    blueplatesdestroyed: int = Field(..., ge=0)
    blueinhibitorsdestroyed: int = Field(..., ge=0)

    bluetotalgold: int = Field(..., ge=0)
    bluetotalexperience: int = Field(..., ge=0)
    bluetotalminionskilled: int = Field(..., ge=0)
    bluetotaljungleminionskilled: int = Field(..., ge=0)


    redwardsplaced: int = Field(..., ge=0)
    redcontrolwardsplaced: int = Field(..., ge=0)
    redwardsdestroyed: int = Field(..., ge=0)
    redcontrolwardsdestroyed: int = Field(..., ge=0)

    redkills: int = Field(..., ge=0)
    reddeaths: int = Field(..., ge=0)
    redassists: int = Field(..., ge=0)

    reddragons: int = Field(..., ge=0)
    redheralds: int = Field(..., ge=0)
    redvoidgrubs: int = Field(..., ge=0)

    redtowersdestroyed: int = Field(..., ge=0)
    redplatesdestroyed: int = Field(..., ge=0)
    redinhibitorsdestroyed: int = Field(..., ge=0)

    redtotalgold: int = Field(..., ge=0)
    redtotalexperience: int = Field(..., ge=0)
    redtotalminionskilled: int = Field(..., ge=0)
    redtotaljungleminionskilled: int = Field(..., ge=0)

    gameduration: float = Field(..., ge=0.0)



class PredictResponse(BaseModel):
    win_probability: float
    win: bool


app = FastAPI(title="league-match-prediction")

with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)


def predict_single(match):
    result = pipeline.predict_proba(match)[0, 1]
    return float(result)


@app.post("/predict")
def predict(match: Match) -> PredictResponse:
    prob = predict_single(match.model_dump())

    return PredictResponse(
        win_probability=prob,
        win=prob >= 0.5
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)