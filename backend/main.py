from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "collected_data.csv")

# ==============================
# Veri Modeli
# ==============================
class GameData(BaseModel):
    correct: int
    wrong: int
    avg_time: float
    hint_used: int

# ==============================
# Veri Toplama Endpoint
# ==============================
@app.post("/collect")
def collect_data(data: GameData):
    new_data = pd.DataFrame([data.dict()])

    if os.path.exists(DATA_PATH):
        new_data.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        new_data.to_csv(DATA_PATH, index=False)

    return {"message": "Data saved successfully"}

# ==============================
# EcoScore Hesaplama Endpoint
# ==============================
@app.post("/predict")
def predict(data: GameData):

    # Matematiksel skor hesaplama
    raw_score = (
        (data.correct * 5)
        - (data.wrong * 3)
        - (data.hint_used * 2)
        - (data.avg_time * 2)
    )

    ecoscore = max(0, min(100, round(raw_score)))

    # Zorluk kararı
    if ecoscore > 70:
        difficulty = "increase"
    elif ecoscore > 45:
        difficulty = "stable"
    else:
        difficulty = "decrease"

    return {
        "ecoscore": ecoscore,
        "difficulty": difficulty
    }