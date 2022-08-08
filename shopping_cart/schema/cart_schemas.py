# 3rd
from pydantic import BaseModel


class Update_Item_quantity(BaseModel):
    product_id: str
    quantity: int


class Cart_Item(BaseModel):
    product_id: str


class Cart_Checkout(BaseModel):
    cart_ids: list[str] = []