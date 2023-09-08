from src.log import logger
from src.utils.db import Base, engine

# 引入所有的表模型以便统一创建
from .user import DBUser  # noqa: F401


def database_init():
    Base.metadata.create_all(engine, checkfirst=True)
    # 创建对象的基类:
    logger.success("Database initialized.")
