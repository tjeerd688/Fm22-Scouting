import os
from pathlib import Path
import pandas as pd
from typing import Union
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import json
import io
import shutil

# Define the path to the "imports" subfolder
UPLOAD_FOLDER = Path("..") / "Api" / "imports"

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

# JSON response of the exported data at the /data URL
@app.get("/data")
def Data():
    # Path to the filtered JSON file
    file_path = Path("..") / "Exports" / "DataFiltered.json"
    # Return JSON data
    with open(file_path, "r") as file:
        return json.load(file)

@app.post("/upload/")
async def upload_csv_file(file: UploadFile = File(...)):
    try:
        # Check if the uploaded file is a CSV
        if not file.filename.endswith(".csv"):
            return JSONResponse(status_code=400, content={"error": "Invalid file type. Please select a CSV file."})

        # Check if the file is empty
        if not file.file:
            return JSONResponse(status_code=400, content={"error": "Empty file. Please select a valid CSV file."})

        # Save the file to the "imports" folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Save the file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)


        # Process the CSV file
        contents = await file.read()

        try:
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        except pd.errors.EmptyDataError:
            return JSONResponse(status_code=400, content={"error": "No columns to parse from file."})

        # Your processing logic goes here

        return {"message": "CSV file uploaded and processed successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
