from datetime import datetime

from pydantic import BaseModel


class _TableName_(BaseModel):
    id: int
    last_update_time: datetime
    created_time: datetime

class OrderOption(BaseModel):
    field_name: str
    desc: bool

class QueryCondition(BaseModel):
    page: int
    page_size: int
    order_by: OrderOption
    keyword: str

class _TableName_Create(BaseModel):
    ...

class _TableName_Update(BaseModel):
    ...

class _TableName_Get(BaseModel):
    id: int

class _TableName_Query(BaseModel):
    condition: QueryCondition

class _TableName_Delete(BaseModel):
    id: int
