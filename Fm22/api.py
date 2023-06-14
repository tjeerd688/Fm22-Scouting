from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
async def root():
    return{'example': 'dit is een voorbeeld', 'data': 0}
    