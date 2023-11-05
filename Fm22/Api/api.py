import os
from pathlib import Path
import numpy as np
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import json
import io
import shutil
import uvicorn
import logging

# defineerd imports folder en json folder
UPLOAD_FOLDER = Path("..") / "Api" / "imports"
EXPORTED_JSON_PATH = Path("C:\\Users\\tjeer\\Documents\\Fm22 Scouting\\Fm22\\Exports\\DataFiltered.json")

#maakt fastapi app
app = FastAPI()

# Cross-origin resource sharing config
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# pakt de huidige tijd
def get_file_timestamp(file_path):
    if file_path.is_file():
        return os.path.getmtime(file_path)
    else:
        return 0  # Return 0 als het bestand niet bestaat

# cleanse de data(uitfilteren)
def cleanse():
    if not csv_file_path.is_file():
        logging.debug("File not found at path: {csv_file_path}")
    else:
        # DataFrame maken en data filteren
        df = pd.read_csv(csv_file_path)
        df = df.replace("-", np.nan)
        df = df.dropna(subset=['Dlp'])
        df = df.sort_values(['Dlp', 'xG'], ascending=[False, False])
        df = df[['Naam', 'Club', 'Dlp', 'xG']]
        df.to_json(EXPORTED_JSON_PATH, orient='index')  # Use EXPORTED_JSON_PATH variable
        logging.debug("Data filtered and exported successfully")

#defineerd pad naar geuploaden csv
csv_file_path = UPLOAD_FOLDER / "data.csv"

@app.get("/")
def read_root():
    return {"Hello": "World"}

#trackt of er een nieuwe csv is geupload
csv_file_uploaded = False

@app.post("/upload/")
async def upload_csv_file(file: UploadFile = File(...)):
    try:
        # controleerd of het verstuurde bestand een CSV is
        if not file.filename.endswith(".csv"):
            return JSONResponse(status_code=400, content={"error": "Invalid file type. Please select a CSV file."})

        # verander input bestandsnaam naar data.csv
        new_filename = "data.csv"

        # slaat data.csv op naar de upload folder]
        file_path = UPLOAD_FOLDER / new_filename

        # slaat bestand op
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        return {"message": "CSV file uploaded successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/data")
def get_data():
    # pakt de tijd van de geuploaden bestand en de laatst geuloaden bestand
    uploaded_file_timestamp = get_file_timestamp(csv_file_path)
    last_processed_file_timestamp = get_file_timestamp(EXPORTED_JSON_PATH)

    if uploaded_file_timestamp > last_processed_file_timestamp:
        # roep de cleanse functie op als de geuploaden bestand nieuwer is
        cleanse()

    # pad naar de json opslaan map om json terug te sturen
    with open(EXPORTED_JSON_PATH, "r") as file:
        data = json.load(file)
    
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
