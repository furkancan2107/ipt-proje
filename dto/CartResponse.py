from pydantic import BaseModel
from dto import ProductResponse
from dto import UserDto

class CartResponse(BaseModel):
    id: int
    product: ProductsResponse
    user: UserDto

    def __init__(self, _id: int, _product: ProductsResponse, _user: UserDto):
        self.id = _id
        self.product = _product
        self.user = _user
