from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.conf import config
from src.models.user import DBUser
from src.schemas.user import TokenData

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = "HS256"


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception  # noqa: B904
    user = DBUser.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: DBUser = Depends(get_current_user),
) -> DBUser:
    expiration_time = current_user.login_time + timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60,
    )

    if expiration_time < datetime.now():  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
