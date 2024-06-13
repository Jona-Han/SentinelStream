from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Transaction(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()

@app.get("/transaction/", status_code=200)
async def read_transaction(transaction: Transaction):
    return