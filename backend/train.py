import pandas as pd
import numpy as np
import os

DATA_PATH = "data/collected_data.csv"

def generate_dummy_data(n=200):
    data = []

    for _ in range(n):
        correct = np.random.randint(0, 20)
        wrong = np.random.randint(0, 20)
        avg_time = np.random.uniform(1.0, 8.0)
        hint_used = np.random.randint(0, 5)

        # Basit mantıkla label üretelim
        score = correct - wrong - hint_used

        if score > 10:
            label = 2  # High
        elif score > 3:
            label = 1  # Medium
        else:
            label = 0  # Low

        data.append([correct, wrong, avg_time, hint_used, label])

    df = pd.DataFrame(data, columns=["correct", "wrong", "avg_time", "hint_used", "label"])

    if os.path.exists(DATA_PATH):
        df.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(DATA_PATH, index=False)

    print("Dummy data generated!")

if __name__ == "__main__":
    generate_dummy_data()