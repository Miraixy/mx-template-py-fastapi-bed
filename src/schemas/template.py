from datetime import datetime
from typing import List

from pydantic import BaseModel


class _TableName_(BaseModel):
    id: int
    last_update_time: datetime
    created_time: datetime

class OrderOption(BaseModel):
    field_name: str
    desc: bool

class FilterOption(BaseModel):
    field_name: str
    value: str

class QueryCondition(BaseModel):
    page: int
    page_size: int
    order_by: OrderOption
    keyword: str
    filters: List[FilterOption]

class _TableName_Create(BaseModel):
    name: str

class _TableName_Update(BaseModel):
    id: int
    name: str

class _TableName_Query(BaseModel):
    condition: QueryCondition
