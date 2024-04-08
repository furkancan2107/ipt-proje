from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from model import User, Product, Cart

class DtoConverter:
    def __init__(self):
        pass

    def convert_user(self, user: User) -> dict:
        if not user:
            return {}
        return {"id": user.id, "username": user.username}

    def convert_product(self, product: Product) -> dict:
        if not product:
            return {}
        return {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "image": product.image,
            "price": product.price,
            "location": product.location,
            "userId": product.user_id,
            "datePosted": product.date_posted,
        }

    def convert_cart(self, cart: Cart) -> dict:
        if not cart:
            return {}
        return {
            "id": cart.id,
            "product": self.convert_product(cart.product),
            "user": self.convert_user(cart.user),
        }
