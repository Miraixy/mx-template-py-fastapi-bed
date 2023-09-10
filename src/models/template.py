from datetime import datetime
from typing import Dict, List

from sqlalchemy import Column, DateTime, Integer, String

from src.schemas.template import QueryCondition
from src.utils.db import Base, db


# 定义User模型
class DB_TableName_(Base):
    __tablename__ = "_table_name_"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 在此添加表结构信息:
    name = Column(String)
    # ...

    last_update_time = Column(DateTime, default=datetime.now)
    created_time = Column(DateTime, default=datetime.now)

    @classmethod
    def add(cls, data: "DB_TableName_"):
        data.last_update_time = datetime.now()
        data.created_time = datetime.now()
        db.add(data)
        db.commit()

    @classmethod
    def get_by_id(cls, _id: int):
        return db.query(cls).filter(cls.id == _id).first()

    @classmethod
    def query(cls, condition: QueryCondition) -> List[Dict]:
        """TODO 实现根据条件查询"""
        raise NotImplementedError

    @classmethod
    def update(cls, data: "DB_TableName_", **kwargs):
        if "id" in kwargs:
            del kwargs["id"]
        if "created_time" in kwargs:
            del kwargs["created_time"]
        if "last_update_time" in kwargs:
            del kwargs["last_update_time"]
        data.last_update_time = datetime.now()
        db.query(cls).filter(cls.id == data.id).update(dict(**kwargs))
        db.commit()

    @classmethod
    def delete(cls, data: "DB_TableName_"):
        db.query(cls).filter(cls.id == data.id).delete()
        db.commit()
