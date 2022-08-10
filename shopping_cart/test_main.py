# built-in
from email import header
import uuid
from random import randint

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

test_item_id = ""
test_all_products = []
test_cart_items = []
test_cart_ids = []

test_user_email = ""
test_user_id = ""
test_user_enkey = "!QAZ2wsx"
user_access_token = ""


def name_generator():
    return uuid.uuid4().hex[-3:]


################## product ##################

def test_create_product():
    create_info = {
        "name": name_generator(),
        "price": randint(1, 100),
        "inventory": randint(1, 50)
    }

    response = client.post("/product",
                        json=create_info)

    assert response.status_code == 200
    assert response.json() == {"msg": "create successfully"}


def test_get_products():
    global test_all_products

    response = client.get("/products")
    assert response.status_code == 200
    
    global test_item_id
    test_item_id = response.json()[-1].get("id")
    test_all_products = response.json()


def test_get_product():
    response = client.get("/product/{}".format(test_item_id))
    assert response.status_code == 200


def test_update_product():
    # 3 param
    update_info = {
        "name": name_generator(),
        "price": randint(1, 100),
        "inventory": randint(1, 50)
    }

    response = client.put("/product/{}".format(test_item_id),
                        json=update_info)

    assert response.status_code == 200
    assert response.json() == {"msg": "update successfully"}

    # 2 param
    update_info = {
        "name": name_generator(),
        "price": randint(1, 100),
    }

    response = client.put("/product/{}".format(test_item_id),
                        json=update_info)

    assert response.status_code == 200
    assert response.json() == {"msg": "update successfully"}

    # 1 param
    update_info = {
        "price": randint(1, 100),
    }

    response = client.put("/product/{}".format(test_item_id),
                        json=update_info)

    assert response.status_code == 200
    assert response.json() == {"msg": "update successfully"}


def test_delete_product():
    response = client.delete("/product/{}".format(test_item_id))
    assert response.status_code == 200
    assert response.json() == {"msg": "delete successfully"}



################## user ##################


def test_create_user():
    global test_user_email
    test_user_email = "{}@test.com".format(name_generator())
    
    create_info = {
        "email": "{}".format(test_user_email),
        "password": "1qaz@WSX",
        "description": "{} test".format(test_user_email),
        "test": "aaaaaaaaaa"
    }

    response = client.post("/signup",
                        json=create_info)

    assert response.status_code == 200
    assert response.json() == {"msg": "create successfully"}


def test_create_duplicate_user():
    name = name_generator()
    create_info = {
        "email": "{}".format(test_user_email),
        "password": "1qaz@WSX",
        "description": "{} test".format(name),
    }

    response = client.post("/signup",
                        json=create_info)

    assert response.status_code == 400
    assert response.json() == {"msg": "email already exist"}


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    
    global test_user_id
    test_user_id = response.json()[-1].get("id")


def test_get_user():
    response = client.get("/user/{}".format(test_user_id))
    assert response.status_code == 200


def test_update_user():
    update_info = {
        "password": "!QAZ2wsx"
    }

    response = client.put("/user/{}".format(test_user_id),
                        json=update_info)

    assert response.status_code == 200
    assert response.json() == {"msg": "update successfully"}



def test_login():
    global user_access_token
    login_info = {
        "username": test_user_email,
        "password": test_user_enkey
    }

    # would send form data when store the 
    response = client.post("/login",
                        data=login_info)
    
    assert response.status_code == 200

    user_access_token = response.json().get("access_token")
    assert user_access_token is not None


def test_get_cart(access_token=None):

    if access_token is None:
        response = client.get("/get_cart/{}".format(test_user_id))
        assert response.status_code == 401

    else:
        global test_cart_ids
        response = client.get("/get_cart/{}".format(test_user_id),
                            headers={"Authorization": "Bearer {}".format(access_token)})
        
        assert response.status_code == 200
        test_cart_ids = response.json()


def test_add_to_cart(access_token=None):
    if access_token is None:
        response = client.put("/add_to_cart/{}".format(test_user_id))
        assert response.status_code == 401

    else:
        global test_cart_items
        rand_idx = randint(0, len(test_all_products)-1)
        product_id = test_all_products[rand_idx].get("id")
        test_cart_items.append(product_id)

        response = client.put("/add_to_cart/{}".format(test_user_id),
                            headers={"Authorization": "Bearer {}".format(access_token)},
                            json={"product_id": product_id})

        assert response.status_code == 200


def test_update_cart_item(access_token=None):
    if access_token is None:
        response = client.put("/update_cart_item/{}".format(test_user_id))
        assert response.status_code == 401

    else:
        rand_idx = randint(0, len(test_all_products)-1)
        product_id = test_all_products[-1]
        
        response = client.put("/update_cart_item/{}".format(test_user_id),
                            headers={"Authorization": "Bearer {}".format(access_token)},
                            json={"product_id": product_id, "quantity": randint(1, 50)})

        if response.status_code == 200:
            assert response.status_code == 200

        else:
            assert response.status_code == 400


def test_del_cart_item(access_token=None):

    if access_token is None:
        response = client.put("/del_cart_item/{}".format(test_user_id))
        assert response.status_code == 401

    else:
        product_id = test_all_products[-1].get("id")
        
        response = client.put("/del_cart_item/{}".format(test_user_id),
                            headers={"Authorization": "Bearer {}".format(access_token)},
                            json={"product_id": product_id})

        print(response.json())
        if response.status_code == 200:
            assert response.status_code == 200

        else:
            assert response.status_code == 400


def test_cart_checkout(access_token=None):
    pass


def test_delete_user():
    response = client.delete("/product/{}".format(test_item_id))
    assert response.status_code == 200
    assert response.json() == {"msg": "delete successfully"}








if __name__ == "__main__":

    # product test
    test_create_product()
    test_get_products()
    test_get_product()
    test_update_product()
    test_get_products()


    # user test
    test_create_user()
    test_create_duplicate_user()
    test_get_users()
    test_get_user()
    test_update_user()
    test_login()

    test_add_to_cart()
    test_add_to_cart(user_access_token)
    test_add_to_cart(user_access_token)
    test_get_cart(user_access_token)
    test_del_cart_item(user_access_token)


