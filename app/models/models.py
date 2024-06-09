from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.db.base import DATABASE_URL
import datetime

Base = declarative_base()


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    fx_id = Column(String, unique=True, index=True)
    code = Column(String, index=True)
    name = Column(String)
    exportOnEshop = Column(Boolean, default=False)
    link = Column(String)

    def __repr__(self):
        return f"<Product(id={self.id}, fx_id={self.fx_id}, code={self.code}, name={self.name}, exportOnEshop={self.exportOnEshop}, link={self.link})>"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, default=None, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables(dev=False):
    if dev:
        Base.metadata.drop_all(bind=engine)

    # Create the table if it doesn't exist
    Base.metadata.create_all(bind=engine)
