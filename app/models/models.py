from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    fx_id = Column(Integer)
    code = Column(String, index=True)
    name = Column(String)
    exportOnEshop = Column(Boolean, default=False)
    link = Column(String)

    def __repr__(self):
        return f"<Product(id={self.id}, code={self.code}, name={self.name}, exportOnEshop={self.exportOnEshop})>"
