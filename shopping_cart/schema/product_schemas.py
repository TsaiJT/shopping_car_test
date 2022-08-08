# 3rd
from pydantic import BaseModel

############ Product ############
# create in/out
class ProductCreateIn(BaseModel):
    name: str
    price: float
    inventory: int


class ProductCreateOut(BaseModel):
    msg: str


#  update in/out
class ProductUpdateIn(BaseModel):
    name: str | None = None
    price: float | None = None
    inventory: int | None = None


class ProductUpdateOut(BaseModel):
    msg: str


# read out
class ProductReadOut(BaseModel):
    id: str
    name: str
    price: float
    inventory: int


class ProductsReadOut(BaseModel):
    products: list[ProductReadOut]


#  delete
class ProductDeleteOut(BaseModel):
    msg: str

