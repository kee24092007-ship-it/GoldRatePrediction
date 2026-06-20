import yfinance as yf
import pandas as pd

gold = yf.download("GC=F", start="2020-01-01", end="2026-01-01")

gold.to_csv("gold_data.csv")

print("Gold data downloaded successfully!")
print(gold.head())