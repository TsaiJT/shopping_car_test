# module
from model.models import session, CartInfo, Order
from model.user_crud import get_user
from model.product_crud import get_product

def create_cart_info(user_obj, product_obj, quantity):

    if quantity > product_obj.inventory:
        return False, "Inventory shortage"

    cart_info = {
        "owner_id": user_obj.id,
        "item_id": product_obj.id,
        "quantity": quantity
    }

    try:
        cart = CartInfo(**cart_info)
        session.add(cart)
        session.commit()

    except Exception as e:
        msg = "{}".format(e)
        return False, "{}".format(e)

    return True, "create successfully"


def add_to_cart(user_id, product_id):
    # get user obj
    is_ok, user = get_user(user_id)
    if not is_ok:
        return False, user

    # get product obj
    is_ok, product = get_product(product_id)
    if not is_ok:
        return False, product

    is_ok, msg = create_cart_info(user, product, 1)
    if not is_ok:
        return False, msg

    return True, "add to cart successfully"


def update_to_cart(user_id, product_id, quantity):
    # get user obj
    is_ok, user = get_user(user_id)
    if not is_ok:
        return False, user

    # get product obj
    is_ok, product = get_product(product_id)
    if not is_ok:
        return False, product

    # get cart obj
    try:
        cart_info = session.query(CartInfo).filter_by(owner_id=user_id, item_id=product_id).first()
        if cart_info is None:
            return False, "add item first"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    if quantity > product.inventory:
        return False, "Inventory shortage"

    # update quantity
    try:
        cart_info.quantity = quantity
        session.commit()

    except Exception as e:
        msg = "{}".format(e)
        return False, "{}".format(e)

    return True, "update successfully"    


def get_cart_info(user_id):
    res = []

    try:
        cart_infos = session.query(CartInfo).filter_by(owner_id=user_id).all()

    except Exception as e:
        msg = "{}".format(e)
        return False, msg
    
    for cart_info in cart_infos:
        tmp = {}
        tmp[cart_info.id] = {} 
        tmp[cart_info.id][cart_info.item_id] = cart_info.quantity

        res.append(tmp)
    
    return True, res


def del_cart_item(user_id, product_id):

    # get user obj
    is_ok, user = get_user(user_id)
    if not is_ok:
        return False, user

    # get product obj
    is_ok, product = get_product(product_id)
    if not is_ok:
        return False, product

    try:
        cart_info = session.query(CartInfo).filter_by(owner_id=user_id, item_id=product_id).first()
        if cart_info is None:
            return False, "no item could be deleted"

        session.delete(cart_info)
        session.commit()

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    return True, "delete item from cart successfully"


def checkout_cart(cart_ids):
    records = []
    total = 0
    owner_id = ""

    for cart_id in cart_ids:
        tmp = {}
        try:
            cart_info = session.query(CartInfo).filter_by(id=cart_id).first()
            if cart_info is None:
                continue

            # get product obj
            is_ok, product = get_product(cart_info.item_id)
            if not is_ok:
                return False, product

            if cart_info.quantity > product.inventory:
                return False, "item not enough"

            if not owner_id:
                owner_id = cart_info.owner_id

        except Exception as e:
            msg = "{}".format(e)
            return False, msg

        tmp["product_id"] = product.id
        tmp["quantity"] = cart_info.quantity
        tmp["cost"] = cart_info.quantity * product.price
        records.append(tmp)
        
        total += tmp["cost"]

    try:
        # reduce inventory
        for record in records:
            # get product obj
            is_ok, product = get_product(record["product_id"])
            if not is_ok:
                session.rollback()
                return False, product

            product.inventory = product.inventory - record["quantity"]
            session.commit()

        # make order
        order = Order(owner_id=owner_id, 
                    record=records, 
                    total=total)

        session.add(order)
        session.commit()

        # delete cart info
        session.query(CartInfo).filter(CartInfo.id.in_(cart_ids)).delete()
        session.commit()


    except Exception as e:
        session.rollback()
        msg = "{}".format(e)
        return False, msg

    return True, "checkout Successfully"



# tmp
def get_user_orders(user_id):
    try:
        user_orders = session.query(Order).filter_by(owner_id=user_id)
        if user_orders is None:
            return False, "user no order information"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    return True, user_orders