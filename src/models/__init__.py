from src.log import logger

# TODO: Import all models that need to be automatically created
from src.models.user import DBUser  # noqa: F401

# $table_create$ 自动创建表追加锚 *请不要修改此行* (Anchor of the table creation line *Do not modify this line*)
from src.utils.db import Base, engine


def database_init():
    Base.metadata.create_all(engine, checkfirst=True)
    # 创建对象的基类:
    logger.success("Database initialized.")
