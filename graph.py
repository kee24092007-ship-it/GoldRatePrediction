import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("gold_data.csv", header=[0,1])

print(data.head())

close_prices = data[("Close", "GC=F")]

plt.figure(figsize=(10,5))
plt.plot(close_prices)
plt.title("Gold Price Trend")
plt.xlabel("Days")
plt.ylabel("Gold Price")
plt.show()