# module
from utils_tool.security_tools import verify_password
from model.user_crud import get_user_by_email

def authenticate_user(email: str, password: str):
    is_ok, user = get_user_by_email(email)
    if not user:
        return False

    if not verify_password(password, user.password):
        return False
        
    return user