import os
import Test1
from pathlib import Path
import numpy as np
import pandas as pd
from typing import Union
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import json
from subprocess import call
import subprocess
import io
import shutil
import uvicorn
import datetime

# Define the path to the "imports" subfolder
UPLOAD_FOLDER = Path("..") / "Api" / "imports"
file_path = Path("..") / "Exports" / "DataFiltered.json"
EXPORTED_JSON_PATH = Path("C:\\Users\\tjeer\\Documents\\Fm22 Scouting\\Fm22\\Exports\\DataFiltered.json")



import logging

# Set up logging
logging.basicConfig(filename='fastapi.log', level=logging.DEBUG)

# Inside your functions, add log messages to track the flow
def cleanse():
    logging.debug("Starting cleanse()")
    # Your cleansing logic
    logging.debug("Finished cleanse()")








app = FastAPI()

# Cross-origin resource sharing configuration
origins = ["*"]
methods = ["GET", "POST", "PUT", "DELETE"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Test response via default HTTP
@app.get("/")
def read_root():
    return {"Hello": "World"}

csv_file_path = UPLOAD_FOLDER / "data.csv"
df = pd.read_csv(csv_file_path)

csv_file_uploaded = False

def cleanse():
    if not csv_file_path.is_file():
        print(f"File not found at path: {csv_file_path}")
    else:
        # DataFrame creation and data processing (assuming the file exists)
        df = pd.read_csv(csv_file_path)
        df = df.replace("-", np.nan)
        df = df.dropna(subset=['Dlp'])
        df = df.sort_values(['Dlp', 'xG'], ascending=[False, False])
        df = df[['Naam', 'Club', 'Dlp', 'xG']]
        df.to_json(EXPORTED_JSON_PATH, orient='index')  # Use EXPORTED_JSON_PATH variable
        print("Data filtered and exported successfully")


cleans_has_run = False
@app.post("/upload/")
async def upload_csv_file(file: UploadFile = File(...)):
    try:
        # Check if the uploaded file is a CSV
        if not file.filename.endswith(".csv"):
            return JSONResponse(status_code=400, content={"error": "Invalid file type. Please select a CSV file."})

        # Set the desired filename (e.g., "data.csv")
        new_filename = "data.csv"

        # Save the file to the "imports" folder with the new filename
        file_path = UPLOAD_FOLDER / new_filename

        # Save the file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        return {"message": "CSV file uploaded successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/data")
def get_data():
    # Get the timestamps of the uploaded file and the last processed file
    uploaded_file_timestamp = get_file_timestamp(UPLOAD_FOLDER / "data.csv")
    last_processed_file_timestamp = get_file_timestamp(EXPORTED_JSON_PATH)

    if uploaded_file_timestamp > last_processed_file_timestamp:
        # Call the cleanse function if the uploaded file is newer
        cleanse()

    # Path to the filtered JSON file
    with open(EXPORTED_JSON_PATH, "r") as file:
        data = json.load(file)
    
    return data

def get_file_timestamp(file_path):
    if file_path.is_file():
        return os.path.getmtime(file_path)
    else:
        return 0  # Return 0 if the file doesn't exist

def cleanse():
    if not csv_file_path.is_file():
        print(f"File not found at path: {csv_file_path}")
    else:
        # DataFrame creation and data processing (assuming the file exists)
        df = pd.read_csv(csv_file_path)
        df = df.replace("-", np.nan)
        df = df.dropna(subset=['Dlp'])
        df = df.sort_values(['Dlp', 'xG'], ascending=[False, False])
        df = df[['Naam', 'Club', 'Dlp', 'xG']]
        df.to_json(EXPORTED_JSON_PATH, orient='index')  # Use EXPORTED_JSON_PATH variable
        print("Data filtered and exported successfully")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


