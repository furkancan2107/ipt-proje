from pydantic import BaseModel

class AddProductRequest(BaseModel):
    title: str
    description: str
    image: str = "default"
    price: float
    location: str
