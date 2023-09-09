import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from src.conf import APP_ENV, config
from src.log import get_logging_config, logger
from src.models import database_init
from src.routers.test import router as test_router

# from src.routers.template import router as template_router
from src.routers.user import login
from src.routers.user import router as user_router
from src.schemas.message import UserToken
from src.schemas.user import UserLogin

database_init()

app = FastAPI(
    title="FastAPI Quickstart",
    description="FastAPI Quickstart",
    version="0.0.1",
    docs_url="/",
)

""" 跨域中间件配置 """
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


""" TODO 挂载路由表 """
app.include_router(user_router, prefix="/user", tags=["User"])
# app.include_router(template_router, prefix="/_table_name_", tags=["_table_name_"])
app.include_router(test_router, prefix="/test", tags=["test"])
... # 请根据需要追加填写


@app.get("/ping")
async def root():
    return {"message": "Miraixy FastAPI Quickstart Running..."}


@app.post("/token", response_model=UserToken)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(
        UserLogin(username=form_data.username, password=form_data.password),
    )


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
