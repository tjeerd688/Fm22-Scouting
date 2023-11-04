#libraries importeren
from fastapi import FastAPI
import json
import pandas as pd
import numpy as np
from pathlib import Path

CSV_PATH = Path("C:\\Users\\tjeer\\Documents\\Fm22 Scouting\\Fm22\\Api\\imports\\data.csv")
EXPORTED_JSON_PATH = Path("C:\\Users\\tjeer\\Documents\\Fm22 Scouting\\Fm22\\Exports\\DataFiltered.json")

def cleanse():
    if not CSV_PATH.is_file():
        print(f"File not found at path: {CSV_PATH}")
    else:
        # DataFrame creation and data processing (assuming the file exists)
        df = pd.read_csv(CSV_PATH)
        df = df.replace("-", np.nan)
        df = df.dropna(subset=['Dlp'])
        df = df.sort_values(['Dlp', 'xG'], ascending=[False, False])
        df = df[['Naam', 'Club', 'Dlp', 'xG']]
        df.to_json('C:\\Users\\tjeer\\Documents\\Fm22 Scouting\\Fm22\\Exports\\DataFiltered.json', orient='index')
        print("Data filtered and exported successfully")

cleanse()







