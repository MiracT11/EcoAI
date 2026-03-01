import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

def generate_regression_dummy(n=200):
    data = []

    for _ in range(n):
        correct = np.random.randint(0, 20)
        wrong = np.random.randint(0, 20)
        avg_time = np.random.uniform(1.0, 8.0)
        hint_used = np.random.randint(0, 5)

        data.append([correct, wrong, avg_time, hint_used])

    df = pd.DataFrame(data, columns=["correct", "wrong", "avg_time", "hint_used"])
    df.to_csv(DATA_PATH, index=False)

    print("Regression dummy data generated!")

DATA_PATH = "data/collected_data.csv"
MODEL_PATH = "models/model.pkl"

def train_model():
    df = pd.read_csv(DATA_PATH)

    X = df[["correct", "wrong", "avg_time", "hint_used"]]

    # Label artık 0-100 arası skor olacak
    y = (
        (df["correct"] * 5)
        - (df["wrong"] * 3)
        - (df["hint_used"] * 2)
        - (df["avg_time"] * 2)
    )

    # 0-100 arası normalize
    y = y.clip(0, 100)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    print(f"Model trained! MSE: {mse:.2f}")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("Model saved successfully!")

if __name__ == "__main__":
    generate_regression_dummy()
    train_model()


   