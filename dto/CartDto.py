from pydantic import BaseModel
from dto import ProductResponse

class CartDto(BaseModel):
    id: int
    product: ProductResponse


