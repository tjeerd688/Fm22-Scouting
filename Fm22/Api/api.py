import os
from pathlib import Path
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

# Define the path to the "imports" subfolder
UPLOAD_FOLDER = Path("..") / "Api" / "imports"
path =  "C:/Users/tjeer/Documents/Fm22 Scouting/Fm22/Main Script/Main.py"
script_path = str(path)
file_path = Path("..") / "Exports" / "DataFiltered.json"




import logging
logging.basicConfig(filename='Main.log', level=logging.INFO)

logging.info("CSV file saved successfully")

logging.info("JSON data exported successfully")




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




@app.post("/upload/")
async def upload_csv_file(file: UploadFile = File(...)):
    try:
        # Check if the uploaded file is a CSV
        if not file.filename.endswith(".csv"):
            return JSONResponse(status_code=400, content={"error": "Invalid file type. Please select a CSV file."})

        # Set the desired filename (e.g., "data.csv")
        new_filename = "data.csv"

        # Check if a file with the same name exists and delete it
        existing_file_path = UPLOAD_FOLDER / new_filename
        if existing_file_path.exists():
            existing_file_path.unlink()

        # Save the file to the "imports" folder with the new filename
        file_path = UPLOAD_FOLDER / new_filename

        # Save the file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Process the CSV file
        contents = await file.read()

        try:
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        except pd.errors.EmptyDataError:
            return JSONResponse(status_code=400, content={"error": "No columns to parse from file."})

        return {"message": "CSV file uploaded and processed successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# JSON response of the exported data at the /data URL
script_has_run = False  # A flag to track whether the script has been executed

def run_script():
    global script_has_run
    if not script_has_run:
        call(["python", str(script_path)])
        script_has_run = True


@app.get("/data")
def get_data():
    run_script()  # Call the script (once)

    # Path to the filtered JSON file
    with open(file_path, "r") as file:
        data = json.load(file)
    
    return data

