# 3rd
from pydantic import BaseModel


class Cart_Info(BaseModel):
    cart_info: dict


class Cart_Item(BaseModel):
    product_ids: list[str] = []


class Cart_Checkout(BaseModel):
    cart_ids: list[str] = []