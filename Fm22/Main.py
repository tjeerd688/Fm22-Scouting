from fastapi import FastAPI
import pandas as pd
import numpy as np
app = FastAPI()

df = pd.read_csv('moneynuts.csv')

df = df.replace("-", np.nan)
df = df.dropna(subset=['Gls'])
df = df.sort_values('Gls', ascending=False)

print(df[['Name','Club','Gls','xG']])
@app.get("/")
async def root():
   return(df[['Name','Club','Gls','xG']])
