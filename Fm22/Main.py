from fastapi import FastAPI
import pandas as pd
import numpy as np
app = FastAPI()

df = pd.read_csv('moneynuts.csv')

df = df.replace("-", pd.np.nan)
df = df.dropna(subset=['Gls'])
df = df.sort_values('Gls', ascending=False)
print(df)

#df_sorted = df.sort_values('column_name')

for index, row in df.iterrows():
    print("index:", index, "Naam:", row['Name'], " Club:", row['Club'], "Goals:", row['Gls']) 


@app.get("/")
async def root():
    return{'Naam': row['Name'],'Club': row['Club'], 'Goals':row['Gls']}

df.to_json(r'C:\Users\tjeer\Documents\Fm22 Scouting\Fm22\Json exports\File Name.json')
