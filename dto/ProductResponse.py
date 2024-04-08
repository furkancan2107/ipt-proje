from pydantic import BaseModel
from typing import Optional
from dto import UserDto

class ProductsResponse(BaseModel):
    id: int
    title: str
    description: str
    image: Optional[str] = "default"
    price: float
    location: str
    user_id: int
    user: UserDto
    date_posted: Optional[str] = None

    def __init__(self, id: int, title: str, description: str, image: str, price: float, location: str, user_id: int, user: UserDto, date_posted: str):
        self.id = id
        self.title = title
        self.description = description
        self.image = image
        self.price = price
        self.location = location
        self.user_id = user_id
        self.user = user
        self.date_posted = date_posted
