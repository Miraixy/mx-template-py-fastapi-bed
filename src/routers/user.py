from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from src.conf import config
from src.log import logger
from src.models.user import DBUser
from src.schemas.message import Ret, UserToken
from src.schemas.user import UserCreate, UserLogin, UserUpdate
from src.utils.auth import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    get_perm_role,
    verify_password,
)
from src.utils.deps import get_current_active_user

ROUTER_TAG = "User"

router = APIRouter()


@router.post("/register", tags=[ROUTER_TAG], summary="用户注册")
async def register(data: UserCreate):
    if data.access_key != config.SUPER_ACCESS_KEY:
        return Ret.fail("Permission denied")
    logger.info(f"User: {data} is registering...")
    if DBUser.get_by_username(data.username):
        return Ret.fail("Username already exists")
    try:
        DBUser.add(
            DBUser(
                username=data.username,
                password=get_hashed_password(data.password),
                perm_level=data.perm_level,
                login_time=None,
            ),
        )
        return Ret.success("Register success")
    except:
        return Ret.fail("Register failed")


@router.post("/login", tags=[ROUTER_TAG], summary="用户登录")
async def login(data: UserLogin):
    user = DBUser.get_by_username(data.username)
    logger.info(f"User: {user.username if user else 'Unknown'} is logging in...")
    if user and verify_password(data.password, user.password):  # type: ignore
        logger.info(f"User {user.username} logging in successfully...")
        DBUser.update(user, login_time=datetime.now())
        return UserToken(
            access_token=create_access_token(user.username),
            refresh_token=create_refresh_token(user.username),
            token_type="bearer",
        )
    logger.info(f"User {data.username} logging in failed...")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/edit", tags=[ROUTER_TAG], summary="用户更新")
async def edit(data: UserUpdate):
    if data.access_key != config.SUPER_ACCESS_KEY:
        return Ret.fail("Permission denied")
    if user := DBUser.get_by_username(data.username):
        model_dict = data.model_dump()
        del model_dict["access_key"]
        del model_dict["username"]
        DBUser.update(user, **model_dict)
        return Ret.success("Update success")
    return Ret.fail("User not found")


@router.get("/me", tags=[ROUTER_TAG], summary="用户个人信息")
async def info(current_user: DBUser = Depends(get_current_active_user)):
    logger.info(f"User: {current_user.username} querying personal information...")
    return Ret.success(
        "query success",
        data={
            "username": current_user.username,
            "userId": current_user.id,
            "perm_level": current_user.perm_level,
            "perm_role": get_perm_role(current_user.perm_level),  # type: ignore
        },
    )

logger.success(f"Successfully initialized {ROUTER_TAG} router")
