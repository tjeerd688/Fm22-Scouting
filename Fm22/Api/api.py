from typing import Union
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/data")
def Data():

    file=open('Json_exports\data_filtered.json',)
    return json.load(file)
