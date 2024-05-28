from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/products")
def get_products():
    pass