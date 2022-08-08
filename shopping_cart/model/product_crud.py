# module
from model.models import session, Product

# c
def create_product(**create_info):
    name = create_info.get("name")
    try:
        product = session.query(Product).filter_by(name=name).first()
        if product:
            return False, "Product name already exist"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg 

    product = Product(**create_info)
    try:
        session.add(product)
        session.commit()

        return True, "create successfully"

    except Exception as e:
        msg = "{}".format(e)
        return False, "{}".format(e)


# u
def update_product(id, **update_info):
    try:
        product = session.query(Product).filter_by(id=id).first()
        if product is None:
            return False, "Product not found"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg 

    if update_info.get("name") is not None:
        product.name = update_info.get("name")

    if update_info.get("price") is not None:
        product.price = update_info.get("price")

    if update_info.get("inventory") is not None:
        product.inventory = update_info.get("inventory")

    try:
        session.commit()
        return True, "update successfully"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg


# r
def get_product(id):
    res = {}
    try:
        product = session.query(Product).filter_by(id=id).first()
        if product is None:
            return False, "Product not found"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    res["id"] = product.id
    res["name"] = product.name
    res["price"] = product.price
    res["inventory"] = product.inventory

    return True, res


def get_products():
    res = []
    try:
        products = session.query(Product).all()
        if products is None:
            return False, "Product not found"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    for product in products:
        tmp = {}
        tmp["id"] = product.id
        tmp["name"] = product.name
        tmp["price"] = product.price
        tmp["inventory"] = product.inventory
        res.append(tmp)

    return True, res

# d
def delete_product(id):
    try:
        del_product = session.query(Product).filter_by(id=id).first()
        if del_product is None:
            return False, "Product not found"
        
        session.delete(del_product)
        session.commit()
        return True, "Delete Successfully"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg