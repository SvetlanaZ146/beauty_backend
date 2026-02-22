from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    ingredients: str

app = FastAPI()
@app.get("/")
def read_root():
    return{"message": "Hellow, FastAPI"}

@app.post("/add_product")
def add_product(product: ProductCreate):
    return {"status": "product added", "product": product}