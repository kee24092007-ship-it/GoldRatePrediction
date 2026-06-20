import pandas as pd

data = pd.read_csv("gold_data.csv", header=[0,1])

close = data[("Close", "GC=F")]

df = pd.DataFrame()
df["Close"] = close

# New Features
df["MA_5"] = df["Close"].rolling(5).mean()
df["MA_10"] = df["Close"].rolling(10).mean()
df["Daily_Return"] = df["Close"].pct_change()

# Tomorrow price
df["Tomorrow"] = df["Close"].shift(-1)

# Target
df["Target"] = (df["Tomorrow"] > df["Close"]).astype(int)

# Remove empty rows
df = df.dropna()

print(df.head())

df.to_csv("prepared_data.csv", index=False)

print("Prepared data saved!")