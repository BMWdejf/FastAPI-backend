from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import DATABASE_URL

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



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)