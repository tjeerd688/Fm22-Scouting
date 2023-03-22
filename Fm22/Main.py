import pandas as pd

df = pd.read_csv('Fm22/Chelsea-export.csv', encoding="utf-8")

print(df.to_string()) 