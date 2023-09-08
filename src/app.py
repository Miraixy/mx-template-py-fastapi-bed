from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.conf import APP_ENV, config
from src.log import get_logging_config, logger
from src.models import database_init
from src.models.user import DBUser
from src.routers.user import router as user_router
from src.schemas.message import UserToken
from src.utils.auth import create_access_token, create_refresh_token, verify_password

database_init()

app = FastAPI(
    title="FastAPI Quickstart",
    description="FastAPI Quickstart",
    version="0.0.1",
    docs_url="/",
)


@app.get("/")
async def root():
    return {"message": "Miraixy FastAPI Quickstart Running..."}


@app.post("/token", response_model=UserToken)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"用户 {form_data.username} 正在登录...")
    user = DBUser.get_by_username(form_data.username)
    if user and verify_password(form_data.password, user.password):  # type: ignore
        DBUser.update(user, login_time=datetime.now())
        return UserToken(
            access_token=create_access_token(user.username),
            refresh_token=create_refresh_token(user.username),
            token_type="bearer",
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# 挂载用户管理路由
app.include_router(user_router, prefix="/user", tags=["User"])


def start():
    logger.info(f"Current environment: {APP_ENV}")
    uvicorn.run(
        "src.app:app",
        host=config.HOST,
        port=config.PORT,
        log_config=get_logging_config(),
        reload=config.RELOAD,
        log_level=config.UVICORN_LOG_LEVEL.lower(),
    )
