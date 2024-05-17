from fastapi import FastAPI
from app.schemas.schemas import products

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/products")
def get_products():
    return products()