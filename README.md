# ENV
ENV: linux-base env
localhost package: docker, docker-compose


# start service
1. `$mkdir -p /opt/shopping_car`
2. copy the package to `/opt/shopping_car`
3. `$cd /opt/shopping_car`
3. `$docker-compose up -d`
4. the service would start up


# test api
* input server_ip:8000/docs in browser could test the apis
* the webpage would show the api description, the parameter that api need and how to use apis


# endpoint

## product
* POST -> /product (create product)
* GET -> /product/{product_id} (get product detail information)
* GET -> /products (get the list of products information)
* PUT -> /product/{product_id} (update product attribute)
* DELETE -> /product/{product_id} (delete the product)


## user
* POST -> /signup (create user)
* GET -> /user/{user_id} (get user detail information)
* GET -> /users (get the list of users information)
* PUT -> /user/{user_id} (update user attribute)
* DELETE -> /user/{user_id} (delete the user)


## login
POST -> /login (user login)
=> would return access, refresh token for the limited api(like cart, checkout)


## cart
* GET -> /get_cart/{user_id} (get cart information by user_id)
* PUT -> /update_to_cart/{user_id} (update/create cart)
* PUT -> /delete_cart_item/{user_id} (delete cart)
* POST -> /cart/checkout (checkout the cart item and create to order table)

