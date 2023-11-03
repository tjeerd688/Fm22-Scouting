#benodige libraries importeren
from typing import Union
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path  
import json

#app defineren
app = FastAPI()

#cross-origin-resource-sharing aanpassen
origins = ["*"]

methods = ["GET", "POST", "PUT", "DELETE"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#test response via onaangepaste http
@app.get("/")
def read_root():
    return {"Hello": "World"}

#json response van de geëxporteerde data op de  http/data url
@app.get("/data")
#met de api request word deze functie uitgevoerd waar de json wordt opgestuurd
def Data():
    #path om het gefilterde json bestand te pakken
    file_path = Path("..") / "Exports" / "DataFiltered.json"
    #json returnen
    with file_path.open("r") as file:
        return json.load(file)


