from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()

DATA_PATH = "data/collected_data.csv"

class GameData(BaseModel):
    correct: int
    wrong: int
    avg_time: float
    hint_used: int

@app.post("/collect")
def collect_data(data: GameData):
    new_data = pd.DataFrame([data.dict()])

    if os.path.exists(DATA_PATH):
        new_data.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        new_data.to_csv(DATA_PATH, index=False)

    return {"message": "Data saved successfully"}