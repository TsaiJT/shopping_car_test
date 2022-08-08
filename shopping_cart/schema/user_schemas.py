# 3rd
from pydantic import BaseModel, EmailStr

############ Product ############
# create in/out
class UserCreateIn(BaseModel):
    email: EmailStr
    password: str
    description: str | None = None


class UserCreateOut(BaseModel):
    msg: str


class UserLogin(BaseModel):
    email: EmailStr


#  update in/out
class UserUpdateIn(BaseModel):
    password: str | None = None
    description: str | None = None


class UserUpdateOut(BaseModel):
    msg: str


# read out
class UserReadOut(BaseModel):
    id: str
    email: EmailStr
    description: str | None = None


class UsersReadOut(BaseModel):
    products: list[UserReadOut]


#  delete
class UserDeleteOut(BaseModel):
    msg: str

