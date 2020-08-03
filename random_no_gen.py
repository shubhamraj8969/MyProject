from typing import Optional

from fastapi import FastAPI
from random import randint

import sys

app = FastAPI()


@app.get("/bhola/{item_id}")
def read_root(item_id: int,q: Optional[str] = None):
    Number = 1
    res = item_id + Number
    return {"RESULT IS": res}

@app.get("/get_number")
def read_number():
    Number = randint(0,sys.maxsize)
    return {"RESULT IS": Number}

