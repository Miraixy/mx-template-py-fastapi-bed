from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.schemas.template import QueryCondition
from src.utils.db import Base, db


# 定义 _TableName_ 模型
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
        """新增 _TableName_ 资源"""

        data.last_update_time = datetime.now()
        data.created_time = datetime.now()
        db.add(data)
        db.commit()

    @classmethod
    def get_by_id(cls, _id: int):
        """根据 id 查询 _TableName_ 资源"""

        return db.query(cls).filter(cls.id == _id).first()

    @classmethod
    def query(cls, condition: QueryCondition):
        """根据条件查询 _TableName_ 资源"""

        page = condition.page if condition.page else 1
        page_size = condition.page_size if condition.page_size else 10
        order_field_name = condition.order_by.field_name
        order_desc = condition.order_by.desc
        keyword = condition.keyword

        query = db.query(cls)

        # for _filter in condition.filters:
        #     field_name = _filter.field_name
        #     value = _filter.value

        #     # TODO 待实现: 检查参数类型，根据不同类型添加不同筛选条件

        if keyword:
            query = db.query(cls).filter(cls.name.like(f"%{keyword}%"))

        if order_field_name:
            query = query.order_by(
                getattr(cls, order_field_name).asc()
                if not order_desc
                else getattr(cls, order_field_name).desc(),
            )

        total = query.count()

        if page and page_size:
            query = query.offset((page - 1) * page_size)
        query = query.limit(page_size)

        return query, total

    @classmethod
    def update(cls, data: "DB_TableName_", **kwargs):
        """更新 _TableName_ 资源"""

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
        """删除 _TableName_ 资源"""

        db.query(cls).filter(cls.id == data.id).delete()
        db.commit()
