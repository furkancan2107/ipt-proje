from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="orders")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")
    order_status = Column(Enum(OrderStatus))

# SQLAlchemy bağlantısı
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Yolları
@app.post("/api/v1/order/create/{userId}/{productId}")
async def create_order(userId: int, productId: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == userId).first()
    db_product = db.query(Product).filter(Product.id == productId).first()
    if not db_user or not db_product:
        raise HTTPException(status_code=400, detail="Ürün sepete eklenemiyor")
    order = Order(product_id=productId, user_id=userId, user=db_user, product=db_product, order_status=OrderStatus.SİPARİŞALINDI)
    db.add(order)
    db.commit()
    return "Sipariş alındı"

@app.delete("/api/v1/order/cancel/{orderId}")
async def cancel_order(orderId: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == orderId).first()
    if not db_order:
        raise HTTPException(status_code=400, detail="Sipariş Bulunamadi")
    db.delete(db_order)
    db.commit()
    return "Sipariş iptal edildi"

@app.put("/api/v1/order/updateOrderStatus/{orderId}")
async def update_order_status(orderId: int, update: UpdateStatusRequest, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == orderId).first()
    if not db_order:
        raise HTTPException(status_code=400, detail="Sipariş Bulunamadi")
    db_order.order_status = update.status
    db.commit()
    return "Durumu güncellendi"

@app.get("/api/v1/order/{userId}")
async def get_my_orders(userId: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == userId).all()
    return orders

@app.get("/api/v1/order/getOrders/{userId}")
async def get_orders(userId: int, db: Session = Depends(get_db)):
    orders = db.query(Order).join(Product, Order.product_id == Product.id).filter(Product.user_id == userId).all()
    return orders
