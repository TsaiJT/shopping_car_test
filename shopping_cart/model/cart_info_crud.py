# module
from model.models import session, User, Product, CartInfo, Order


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

        return True, "create successfully"

    except Exception as e:
        msg = "{}".format(e)
        return False, "{}".format(e)


def update_cart_info(cart_info, product_obj, quantity):

    if quantity > product_obj.inventory:
        return False, "Inventory shortage"

    if cart_info.quantity == quantity:
        return False, "no need to update"

    try:
        cart_info.quantity = quantity
        session.add(cart_info)
        session.commit()

        return True, "create successfully"

    except Exception as e:
        msg = "{}".format(e)
        return False, "{}".format(e)



def update_to_cart(user_id, cart_infos):
    # get user obj
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user is None:
            return False, "not found"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    # check each product id
    for product_id in cart_infos:
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            print(product.id)
            if product is None:
                return False, "{} not found".format(product_id)

        except Exception as e:
            msg = "{}".format(e)
            return False, msg

        try:
            cart_info = session.query(CartInfo).filter_by(owner_id=user_id, item_id=product_id).first()
            quantity = cart_infos[product_id]
            if cart_info is None:
                is_ok, msg = create_cart_info(user, product, quantity)
                if not is_ok:
                    return False, msg

            else:
                is_ok, msg = update_cart_info(cart_info, product, quantity)
                if not is_ok:
                    return False, msg

        except Exception as e:
            msg = "{}".format(e)
            return False, msg

    return True, "cart info update successfully"


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


def del_cart_item(user_id, product_ids):

    # get user obj
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user is None:
            return False, "not found"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    count = 0
    for product_id in product_ids:
        try:
            cart_info = session.query(CartInfo).filter_by(owner_id=user_id, item_id=product_id).first()
            if cart_info is None:
                continue

            session.delete(cart_info)
            session.commit()

            count += 1
        except Exception as e:
            msg = "{}".format(e)
            return False, msg

    if count == 0:
        return False, "not item in cart"
    
    return True, "delete Successfully"


def checkout_cart(cart_ids):
    record = {}
    tmp_total = 0
    owner_id = ""

    for cart_id in cart_ids:
        tmp = {}
        try:
            cart_info = session.query(CartInfo).filter_by(id=cart_id).first()
            if cart_info is None:
                continue

            product = session.query(CartInfo).filter_by(id=cart_info.item_id).first()
            if product is None:
                return False, "inventory shortage"
            if cart_info.quantity > product.inventory:
                return False, "product not exist"

            if not owner_id:
                owner_id = cart_info.owner_id

        except Exception as e:
            msg = "{}".format(e)
            return False, msg

        tmp["product_id"] = product.id
        tmp["product_id"]["quantity"] = cart_info.quantity
        tmp["product_id"]["cost"] = cart_info.quantity * product.price
        tmp_total += tmp["product_id"]["cost"]

    session.begin()
    try:
        order = Order(owner_id=owner_id, record=record)
        session.add(order)
        session.commit()

        session.query(CartInfo).filter(CartInfo.id.in_(cart_ids)).delete()
        session.commit()


    except Exception as e:
        session.rollback()
        msg = "{}".format(e)
        return False, msg

    return True, "checkout Successfully"