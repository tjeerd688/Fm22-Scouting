#benodige libraries importeren
from typing import Union
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
#test response via on aangepaste http
@app.get("/")
def read_root():
    return {"Hello": "World"}

#json response van de geëxporteerde data op de  http/data url
@app.get("/data")
#met de api request word deze functie uitgevoerd waar de json wordt opgestuurd
def Data():
    
    file=open(r'C:\Users\tjeer\Documents\Fm22 Scouting\Fm22\Main Script\Json_exports\DataFiltered.json',"r")

    return json.load(file)

