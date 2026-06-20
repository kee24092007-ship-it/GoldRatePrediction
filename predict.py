import joblib
import pandas as pd

model = joblib.load("gold_model.pkl")

# Example input (latest values)
data = pd.DataFrame([[3400, 3395, 3380, 0.002]],
                    columns=["Close", "MA_5", "MA_10", "Daily_Return"])

prediction = model.predict(data)

if prediction[0] == 1:
    print("Gold Price will go UP 📈")
else:
    print("Gold Price will go DOWN 📉")