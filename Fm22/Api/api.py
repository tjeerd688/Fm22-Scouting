from typing import Union
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json


app = FastAPI()

origins = ["*"]

methods = ["GET", "POST", "PUT", "DELETE"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],


)




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/data")
def Data():
    
    file=open(r'C:\Users\tjeer\Documents\Fm22 Scouting\Fm22\Main Script\Json_exports\DataFiltered.json',"r")

    return json.load(file)

@app.get("/test")
def Data():

    file=open(r'C:\Users\tjeer\Documents\Fm22 Scouting\Fm22\Main Script\Json_exports\DataFiltered.json',"r")

    return json.load(file)