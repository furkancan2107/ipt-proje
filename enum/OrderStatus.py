from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class OrderStatus(str, Enum):
    SIPARIS_ALINDI = "Sipariş Alındı"
    ONAYLANDI = "Onaylandı"
    KARGODA = "Kargoda"
    TESLIM_EDILDI = "Teslim Edildi"

@app.get("/orders/{order_id}")
async def read_order(order_id: int, status: OrderStatus):
    return {"order_id": order_id, "status": status}
