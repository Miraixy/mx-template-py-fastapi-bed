from src.log import logger

# TODO 引入所有需要自动创建的表模型
from src.models.user import DBUser  # noqa: F401

# $table_create$ 自动创建表追加锚 请不要修改此行*
from src.utils.db import Base, engine


def database_init():
    Base.metadata.create_all(engine, checkfirst=True)
    # 创建对象的基类:
    logger.success("Database initialized.")
