from app.models.models import SessionLocal
from app.services.user_service import UserService


def get_user_service():
    with SessionLocal.begin() as session:
        yield UserService(session)
