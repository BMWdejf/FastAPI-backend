from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str
