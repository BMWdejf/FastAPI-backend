import sqlalchemy

from app.models.models import User
from app.schemas.schemas import CreateUserSchema, LoginSchema
from app.utils.exceptions import EmailDuplicationException, UserNotFoundException
from app.utils.password import hash_password, verify_password
from sqlalchemy.orm import Session
from sqlalchemy import exc, select


class UserService:
    def __init__(self, session: Session):
        self.session = session

    async def login(self, data: LoginSchema):
        user = await self.get_by_username(data.username)

        if not user:
            raise UserNotFoundException("Username or password is invalid")

        if not verify_password(data.password, user.password.encode("utf-8")):
            raise UserNotFoundException("Username or password is invalid")

        return user

    async def create_user(self, data: CreateUserSchema):
        try:
            new_user = User(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                username=data.username,
                password=hash_password(data.password).decode("utf-8"),
            )

            self.session.add(new_user)
            self.session.commit()

            return new_user
        except exc.IntegrityError as e:
            print(e)
            raise EmailDuplicationException(f"Email [{data.email}] already exists")
        except Exception as e:
            print(e)
            raise Exception(e)

    async def get_by_username(self, username: str):
        query = (
            select(User.user_id, User.username, User.email, User.password)
            .where(User.username == username)
            .limit(1)
        )

        result = self.session.execute(query)
        return result.first()
