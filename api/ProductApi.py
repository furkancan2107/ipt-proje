from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from typing import List

# SQLAlchemy modelleri
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, default="default")
    price = Column(String, nullable=False)
    location = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="products")


class DContext:
    def __init__(self):
        SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()


# Dependency
def get_db():
    db = DContext()
    try:
        yield db
    finally:
        db.close()


# FastAPI uygulaması
app = FastAPI()


# Pydantic modelleri
class AddProductRequest(BaseModel):
    title: str
    description: str
    image: str
    price: float
    location: str
    user_id: int


class UpdateProductRequest(BaseModel):
    title: str
    description: str
    price: float
    location: str


class ProductsResponse(BaseModel):
    id: int
    title: str
    description: str
    image: str
    price: float
    location: str
    user_id: int


# API Yolları
@app.post("/api/v1/product/add/{user_id}")
async def add_product(user_id: int, product_request: AddProductRequest, db: DContext = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Kullanici Bulunamadi")
    db_product = Product(**product_request.dict(), user=user)

