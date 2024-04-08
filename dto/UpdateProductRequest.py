from pydantic import BaseModel
from typing import Optional

class UpdateProductRequest(BaseModel):
    title: str
    description: str
    price: float
    location: Optional[str] = None
