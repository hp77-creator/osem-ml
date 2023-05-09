from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get('/ml')
def read_ml():
    return {"ML":"Model"}
