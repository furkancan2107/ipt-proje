from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
import random
from typing import Optional

# SQLAlchemy modelleri
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    activation_code = Column(String, default="default")

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

# Şifreleme için kullanılacak nesne
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic modelleri
class CreateUserDto(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ChangePasswordRequest(BaseModel):
    activation_code: str
    new_password: str

# API Yolları
@app.post("/api/v1/user/create")
async def create_user(user: CreateUserDto, db: DContext = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Bu mail zaten kayıtlı")
    return {"message": "Başari ile kayıt olundu"}

@app.post("/api/v1/user/login")
async def login(login_request: LoginRequest, db: DContext = Depends(get_db)):
    db_user = db.query(User).filter(User.email == login_request.email).first()
    if not db_user or not pwd_context.verify(login_request.password, db_user.password):
        raise HTTPException(status_code=400, detail="Kullanıcı bulunamadı veya şifre hatalı")
    return {"user_id": db_user.id}

@app.put("/api/v1/user/forgot")
async def forgot_password(email: ForgotPasswordRequest, db: DContext = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Kullanici Bulunamadi")
    activation_code = str(random.randint(100000, 999999))
    db_user.activation_code = activation_code
    db.commit()
    # Mail gönderme işlemi buraya eklenecek
    return {"message": "Aktivasyon kodunuz mail adresinize gönderildi"}

@app.put("/api/v1/user/changePassword/{email}")
async def change_password(email: str, change_password_request: ChangePasswordRequest, db: DContext = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or db_user.activation_code != change_password_request.activation_code:
        raise HTTPException(status_code=400, detail="Sistem hatası veya hatalı kod girdiniz")
    hashed_password = pwd_context.hash(change_password_request.new_password)
    db_user.password = hashed_password
    db_user.activation_code = "default"
    db.commit()
    return {"message": "Şifre başarı ile değiştirildi"}

@app.delete("/api/v1/user/{id}")
async def delete_user(id: int, db: DContext = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Kullanici Bulunamadi")
    db.delete(db_user)
    db.commit()
    return {"message": "Kullanici başarı ile silindi"}
