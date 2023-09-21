from fastapi import FastAPI
import json
import pandas as pd
import numpy as np
app = FastAPI()

kms = input("Welke statistiek wilt U zien? Ast ")
df = pd.read_csv('Main script/data.csv')

df = df.replace("-", np.nan)

df = df.dropna(subset=['Dlp'])
#sorting van Goals en Subsort van xG
df = df.sort_values(['Dlp','xG'], ascending=[False,False])
df = df[['Naam','Club','Dlp','xG',kms]]
print(df)
df.to_json(r'C:\Users\tjeer\Documents\Fm22 Scouting\Fm22\Json_exports/data_filtered.json')
