#built-in
from datetime import datetime, timedelta

# 3rd
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


# module
from schema.token_schemas import TokenData
from schema.user_schemas import UserLogin

from model.user_crud import get_user_by_email

from config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, 
                            settings.JWT_SECRET_KEY, 
                            algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, 
                            settings.JWT_REFRESH_SECRET_KEY, 
                            algorithm=settings.ALGORITHM)
    return encoded_jwt



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                            settings.JWT_SECRET_KEY,
                            algorithms=[settings.ALGORITHM])
        email: str = payload["sub"]
        exp: int = payload["exp"]
    except JWTError:
        raise credentials_exception

    if datetime.fromtimestamp(exp) < datetime.now():
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if email is None:
        raise credentials_exception
    token_data = TokenData(email=email)

    is_ok, user = get_user_by_email(email)
    if not is_ok:
        raise credentials_exception

    return user