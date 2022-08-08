# module
from model.models import session, User, Product

from utils_tool.security_tools import get_password_hash

# c
def create_user(**create_info):
    email = create_info.get("email")
    try:
        product = session.query(User).filter_by(email=email).first()
        if product:
            return False, "email already exist"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg 

    create_info["password"] = get_password_hash(create_info["password"])

    try:
        user = User(**create_info)
        session.add(user)
        session.commit()

        return True, "create successfully"

    except Exception as e:
        msg = "{}".format(e)
        return False, "{}".format(e)


# u
def update_user(id, **update_info):
    try:
        user = session.query(User).filter_by(id=id).first()
        if user is None:
            return False, "not found"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg 


    if update_info.get("password") is not None:
        user.password = get_password_hash(update_info.get("password"))

    if update_info.get("description") is not None:
        user.description = update_info.get("description")


    try:
        session.commit()
        return True, "update successfully"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg



# r
def get_user(id):
    res = {}
    try:
        user = session.query(User).filter_by(id=id).first()
        if user is None:
            return False, "not found"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    res["id"] = user.id
    res["email"] = user.email
    res["description"] = user.description

    return True, res

def get_user_by_email(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        if user is None:
            return False, "email not found"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    return True, user


def get_users():
    res = []
    try:
        users = session.query(User).all()
        if users is None:
            return False, "no users information"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg

    for user in users:
        tmp = {}
        tmp["id"] = user.id
        tmp["email"] = user.email
        tmp["description"] = user.description

        res.append(tmp)

    return True, res



# d
def delete_user(id):
    try:
        del_user = session.query(User).filter_by(id=id).first()
        if del_user is None:
            return False, "email not found"
        
        session.delete(del_user)
        session.commit()
        return True, "delete Successfully"

    except Exception as e:
        msg = "{}".format(e)
        return False, msg