from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    activation_code: str = "default"  # C#'daki ActivationCode özelliği için uygun Python adı
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
