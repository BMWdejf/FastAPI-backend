from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.flexibee_api_url import import_products
from app.utils.auth import get_current_user, authenticate_user, create_access_token, Token, db, timedelta, ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.models import Products

app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/import_products")
async def import_products_endpoint(user: str = Depends(get_current_user)):
    await import_products()
    return {"message": "Products imported successfully"}


@app.get("/products")
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Products).all()
    get_products = [{"fx_id": product.fx_id, "code": product.code, "name": product.name, "link": product.link} for
                         product in products]
    return get_products