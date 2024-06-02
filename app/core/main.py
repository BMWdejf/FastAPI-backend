from fastapi import FastAPI, Depends
from app.utils.authentication import verify_token
from app.db.flexibee_api_url import get_data as import_products_function

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/import_products")
async def import_products_endpoint(valid_token: bool = Depends(verify_token)):
    await import_products_function()
    return {"message": "Products imported successfully"}