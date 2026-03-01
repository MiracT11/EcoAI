from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import pickle

app = FastAPI()

DATA_PATH = "data/collected_data.csv"
MODEL_PATH = "models/model.pkl"

# ==============================
# Veri Modeli
# ==============================
class GameData(BaseModel):
    correct: int
    wrong: int
    avg_time: float
    hint_used: int

# ==============================
# Model Global Değişken
# ==============================

model = None

# ==============================
# Startup Event – Modeli Yükle
# ==============================
@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("✅ Model loaded successfully!")
    else:
        print("⚠️ Model file not found. Train the model first.")

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
# Tahmin Endpoint
# ==============================
@app.post("/predict")
def predict(data: GameData):
    global model

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    input_df = pd.DataFrame([{
        "correct": data.correct,
        "wrong": data.wrong,
        "avg_time": data.avg_time,
        "hint_used": data.hint_used
    }])

    prediction = model.predict(input_df)[0]

    ecoscore = max(0, min(100, round(prediction)))

    if ecoscore > 75:
        difficulty = "increase"
    elif ecoscore > 40:
        difficulty = "stable"
    else:
        difficulty = "decrease"

    return {
        "ecoscore": ecoscore,
        "difficulty": difficulty
    }