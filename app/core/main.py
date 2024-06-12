import json
from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from contextlib import asynccontextmanager
from app.schemas.schemas import CreateUserSchema, LoginSchema
from app.services.user_service import UserService
from app.utils.deps import get_user_service
from app.utils.exceptions import InvalidData, EmailDuplicationException, UsernameDuplicationException, UserNotFoundException
from app.utils.jwt_token import create_access_token
from app.utils.user import get_current_user
from app.db.flexibee_api_url import import_products
from sqlalchemy.orm import Session
from app.db.base import get_db
from sqlalchemy.exc import NoResultFound
from app.models.models import Products, create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
router = APIRouter()

@router.post("/login")
async def login(*, user_service: UserService = Depends(get_user_service), request: LoginSchema):
    try:
        user = await user_service.login(request)

        access_token = create_access_token(
            data={"sub": user.username},
        )
        return Response(status_code=status.HTTP_200_OK, content=json.dumps({"access_token": access_token, "token_type": "bearer"}))
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or username")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "message": "Something went wrong",
            "code": "INTERNAL_SERVER_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        })


@router.post("/users", response_class=Response, status_code=status.HTTP_201_CREATED)
async def create_user(*, user_service: UserService = Depends(get_user_service), request: CreateUserSchema):
    try:
        await user_service.create_user(request)
        return Response(status_code=status.HTTP_201_CREATED)
    except InvalidData as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "message": str(e),
            "code": "INVALID_DATA",
            "status_code": status.HTTP_400_BAD_REQUEST,
        })
    except EmailDuplicationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "message": str(e),
            "code": "EMAIL_DUPLICATION",
            "status_code": status.HTTP_409_CONFLICT,
        })
    except UsernameDuplicationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "message": str(e),
            "code": "USERNAME_DUPLICATION",
            "status_code": status.HTTP_409_CONFLICT,
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "message": "Something went wrong",
            "code": "INTERNAL_SERVER_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        })


@router.get("/import_products")
async def import_products_endpoint(_: str = Depends(get_current_user)):
    await import_products()
    return {"message": "Products imported successfully"}


@router.get("/products")
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Products).all()
    get_products = [{"fx_id": product.fx_id, "code": product.code, "name": product.name, "link": product.link} for product in products]
    return get_products


@router.get("/product/{id}")
async def get_product_by_fx_id(id: str, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.fx_id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    get_product = {"id": product.fx_id, "code": product.code, "name": product.name, "link": product.link}
    return get_product


app.include_router(router)