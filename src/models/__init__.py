from src.log import logger
from src.utils.db import Base, engine

# TODO 引入所有需要自动创建的表模型
# from .template import DB_TableName_  # noqa: F401
from .test import DBTest  # noqa: F401
from .user import DBUser  # noqa: F401

...


def database_init():
    Base.metadata.create_all(engine, checkfirst=True)
    # 创建对象的基类:
    logger.success("Database initialized.")
