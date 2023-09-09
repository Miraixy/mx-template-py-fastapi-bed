from sqlalchemy import Column, DateTime, Integer, String

from src.utils.db import Base, db


# 定义User模型
class DBUser(Base):
    # 表的名字:
    __tablename__ = "user"

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)  # noqa: A003
    username = Column(String(32))
    password = Column(String(32))
    perm_level = Column(Integer())
    login_time = Column(DateTime)

    @classmethod
    def add(cls, data: "DBUser"):
        db.add(data)
        db.commit()

    @classmethod
    def get_by_username(cls, username: str):
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def update(cls, data: "DBUser", **kwargs):
        db.query(cls).filter(cls.username == data.username).update(dict(**kwargs))
        db.commit()

    @classmethod
    def delete(cls, data: "DBUser"):
        db.query(cls).filter(cls.username == data.username).delete()
        db.commit()
