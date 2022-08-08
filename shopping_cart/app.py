# built-in
import datetime

# 3rd
import uvicorn
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt


# module 
from fastapi_init import app
from config import settings
from utils_tool.common_tools import return_message
from utils_tool.authenticate_tools import authenticate_user
from utils_tool.jwt_tools import create_access_token, create_refresh_token, \
                                get_current_user

from schema.product_schemas import ProductReadOut, ProductsReadOut, \
                                ProductCreateIn, ProductCreateOut, \
                                ProductUpdateIn, ProductUpdateOut, \
                                ProductDeleteOut
from schema.user_schemas import UserReadOut, UsersReadOut, \
                                UserCreateIn, UserCreateOut, \
                                UserUpdateIn, UserUpdateOut, \
                                UserDeleteOut, UserLogin
from schema.token_schemas import Token
from schema.cart_schemas import Cart_Info, Cart_Item, Cart_Checkout

from model.product_crud import create_product, update_product, \
                                get_product, get_products, delete_product
from model.user_crud import create_user, update_user, \
                            get_user, get_users, delete_user
from model.cart_info_crud import update_to_cart, get_cart_info, del_cart_item, checkout_cart




@app.post("/product", response_model=ProductCreateOut)
async def product_creater(product: ProductCreateIn):
    result = {}

    is_ok, res = create_product(**dict(product))
    result["msg"] = res

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


@app.put("/product/{product_id}", response_model=ProductUpdateOut)
async def product_updater(product_id: str, product: ProductUpdateIn):
    result = {}

    is_ok, msg = update_product(product_id, **dict(product))
    result["msg"] = msg

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


@app.get("/product/{product_id}", response_model=ProductReadOut)
async def product_getter(product_id: str):
    is_ok, result = get_product(product_id)

    status_code = 200
    if not is_ok:
        result = {"msg": result}
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


@app.get("/products", response_model=ProductsReadOut)
async def products_getter():
    is_ok, result = get_products()

    status_code = 200
    if not is_ok:
        result = {"msg": result}
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)



@app.delete("/product/{product_id}", response_model=ProductDeleteOut)
async def product_deleter(product_id: str):
    result = {}

    is_ok, msg = delete_product(id=product_id)
    result["msg"] = msg

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)



@app.post("/signup", response_model=UserCreateOut)
async def user_creater(user: UserCreateIn):
    result = {}

    is_ok, res = create_user(**dict(user))
    result["msg"] = res

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


@app.put("/user/{user_id}", response_model=UserUpdateOut)
async def user_updater(user_id: str, user: UserUpdateIn):
    result = {}

    is_ok, msg = update_user(user_id, **dict(user))
    result["msg"] = msg

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


@app.get("/user/{user_id}", response_model=UserReadOut)
async def user_getter(user_id: str):
    is_ok, result = get_user(user_id)
    print(result)

    status_code = 200
    if not is_ok:
        result = {"msg": result}
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


@app.get("/users", response_model=UsersReadOut)
async def users_getter():
    is_ok, result = get_users()

    status_code = 200
    if not is_ok:
        result = {"msg": result}
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


@app.delete("/user/{user_id}", response_model=UserDeleteOut)
async def user_deleter(user_id: str):
    result = {}

    is_ok, msg = delete_user(id=user_id)
    result["msg"] = msg

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


@app.post("/login", response_model=Token)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


    res = {
        "access_token": create_access_token({"sub": user.email}),
        "refresh_token": create_refresh_token({"sub": user.email})
    
    }

    return JSONResponse(status_code=200, 
                        content=res)


@app.get("/get_cart/{user_id}")
async def get_cart(user_id: str,
                    current_user: UserLogin = Depends(get_current_user)):
    result = {}

    is_ok, msg = get_cart_info(user_id)
    result["msg"] = msg

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result) 


@app.put("/update_to_cart/{user_id}")
async def update_cart(user_id: str, 
                    cart_info: Cart_Info,
                    current_user: UserLogin = Depends(get_current_user)):
    
    result = {}

    is_ok, msg = update_to_cart(user_id, cart_info.cart_info)
    result["msg"] = msg

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)

@app.put("/del_cart_item/{user_id}")
async def cart_item_delete(user_id: str, 
                     product_ids: Cart_Item,
                    current_user: UserLogin = Depends(get_current_user)):
    
    result = {}

    is_ok, msg = del_cart_item(user_id, product_ids.product_ids)
    result["msg"] = msg

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


@app.post("/cart_checkout")
async def cart_checkout(cart_id: Cart_Checkout,
                        current_user: UserLogin = Depends(get_current_user)):
    result = {}

    is_ok, msg = checkout_cart(cart_ids.cart_ids)
    result["msg"] = msg

    status_code = 200
    if not is_ok:
        status_code = 400

    return JSONResponse(status_code=status_code, 
                        content=result)


if __name__ == "__main__":
    uvicorn.run(app, 
                host="0.0.0.0", 
                port=settings.PORT)