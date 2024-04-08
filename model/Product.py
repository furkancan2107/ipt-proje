import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    image = Column(String, default="default")
    price = Column(DECIMAL)
    location = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))  # users tablosuna referans
    user = relationship("User", back_populates="products")  # users tablosuyla ilişki
    date_posted = Column(DateTime, default=datetime.datetime.utcnow)


