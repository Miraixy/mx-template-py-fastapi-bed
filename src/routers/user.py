from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from src.conf import config
from src.deps import get_current_active_user
from src.log import logger
from src.models.user import DBUser
from src.schemas.message import Ret, UserToken
from src.schemas.user import UserCreate, UserLogin
from src.utils.auth import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)

router = APIRouter()


@router.post("/register", tags=["User"], summary="用户注册")
async def register(data: UserCreate):
    if data.access_key != config.SUPER_ACCESS_KEY:
        return Ret.fail("权限不足")
    logger.info(f"用户 {data} 正在注册...")
    if DBUser.get_by_username(data.username):
        return Ret.fail("用户名已存在")
    try:
        DBUser.add(
            DBUser(
                username=data.username,
                password=get_hashed_password(data.password),
                perm_level=data.perm_level,
                login_time=None,
            ),
        )
        return Ret.success("注册成功")
    except:
        return Ret.fail("注册失败")


@router.post("/login", tags=["User"], summary="用户登录")
async def login(data: UserLogin):
    user = DBUser.get_by_username(data.username)
    logger.info(f"用户 {user} 正在登录...")
    if user and verify_password(data.password, user.password):  # type: ignore
        logger.info(f"用户 {user} 登录成功...")
        DBUser.update(user, login_time=datetime.now())
        return UserToken(
            access_token=create_access_token(user.username),
            refresh_token=create_refresh_token(user.username),
            token_type="bearer",
        )
    logger.info(f"用户 {user} 登录失败... ")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/me", tags=["User"], summary="用户个人信息")
async def info(current_user: DBUser = Depends(get_current_active_user)):
    logger.info(f"用户 {current_user} 正在查询个人信息...")
    return Ret.success("query success", data={"username": current_user.username})
