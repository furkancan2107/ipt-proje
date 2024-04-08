from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from dto import ProductResponse

# SQLAlchemy modelleri
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="carts")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="carts")

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
class CartDto(BaseModel):
    id: int
    product: ProductResponse

class AddCartRequest(BaseModel):
    userId: int
    productId: int

# API Yolları
@app.post("/api/v1/cart/addCart/{userId}/{productId}")
async def add_cart(userId: int, productId: int, db: DContext = Depends(get_db)):
    db_user = db.query(User).filter(User.id == userId).first()
    db_product = db.query(Product).filter(Product.id == productId).first()
    if not db_user or not db_product:
        raise HTTPException(status_code=400, detail="Kullanici veya ürün bulunamadi")
    db_cart = Cart(user=db_user, product=db_product)
    db.add(db_cart)
    db.commit()
    return "Ürün Sepete Eklendi"

@app.delete("/api/v1/cart/removeCart/{cartId}")
async def remove_cart(cartId: int, db: DContext = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cartId).first()
    if not db_cart:
        raise HTTPException(status_code=400, detail="Ürün sepette değil")
    db.delete(db_cart)
    db.commit()
    return "Ürün Silindi"

@app.get("/api/v1/cart/carts/{userId}")
async def get_cart_list(userId: int, db: DContext = Depends(get_db)):
    carts = db.query(Cart).filter(Cart.user_id == userId).all()
    cart_list = []
    for cart in carts:
        product = db.query(Product).filter(Product.id == cart.product_id).first()
        if product:
            cart_list.append(CartDto(id=cart.id, product=product))
    return cart_list
