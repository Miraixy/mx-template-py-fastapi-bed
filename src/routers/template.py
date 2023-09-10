from fastapi import APIRouter, Depends, HTTPException, status

from src.conf import config  # noqa: F401
from src.log import logger
from src.models.template import DB_TableName_
from src.models.user import DBUser
from src.schemas.message import Ret
from src.schemas.perm import Role
from src.schemas.template import (
    _TableName_Create,
    _TableName_Delete,
    _TableName_Query,
    _TableName_Update,
)
from src.utils.deps import get_current_active_user

ROUTER_TAG = "_Table_name_"

router = APIRouter()


@router.post("/create", tags=[ROUTER_TAG], summary="创建")
async def create(data: _TableName_Create):
    """创建 _TableName_ 资源"""
    try:
        item = DB_TableName_(**data.model_dump())
        DB_TableName_.add(item)
        return Ret.success(
            "创建成功",
            data={
                "id": item.id,
                "name": item.name,
                "last_update_time": item.last_update_time,
                "created_time": item.created_time,
            },
        )
    except:
        logger.error(f"创建 {data} 资源时发生错误")
        return Ret.fail("创建失败")


@router.get("/detail", tags=[ROUTER_TAG], summary="查询详情")
async def get(_id):
    """根据 id 查询 _TableName_ 资源"""

    item = DB_TableName_.get_by_id(_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Ret.success(
        "query success",
        data={
            "id": item.id,
            "name": item.name,
            "last_update_time": item.last_update_time,
            "created_time": item.created_time,
        },
    )


@router.post("/list", tags=[ROUTER_TAG], summary="检索分页")
async def query(data: _TableName_Query):
    """根据条件检索 _TableName_ 资源"""

    try:
        # TODO DB_TableName_.query 方法默认提供了分页、排序、关键字过滤，如果需要其他条件需自行实现
        try:
            items = DB_TableName_.query(data.condition)
        except Exception as e:
            logger.error(f"检索资源 {data} 时发生错误: {e}")
            return Ret.fail("检索资源出现错误，请检查参数字段是否正确")

        return Ret.success(
            "query success",
            data=[{
                "id": item.id,
                "name": item.name,
                "created_time": item.created_time,
                "last_update_time": item.last_update_time,
            } for item in items],
        )
    except Exception as e:
        logger.error(f"检索资源 {data} 资源时发生错误: {e}")
        return Ret.fail("检索资源失败")


@router.put("/update", tags=[ROUTER_TAG], summary="更新数据")
async def update(data: _TableName_Update):
    """根据 id 更新 Example 资源"""
    item = DB_TableName_.get_by_id(data.id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    try:
        update_data = data.model_dump()
        # ... 处理更新

        DB_TableName_.update(item, **update_data)
        return Ret.success("更新成功", data={"id": item.id, "name": item.name})
    except Exception as e:
        logger.error(f"更新 {data} 资源时发生错误: {e}")
        return Ret.fail("更新失败")


@router.delete("/delete", tags=[ROUTER_TAG], summary="删除数据")
async def delete(data: _TableName_Delete, current_user: DBUser = Depends(get_current_active_user)):
    """根据 id 删除 _TableName_ 资源"""
    if current_user.perm_level < Role.Admin: # type: ignore
        return Ret.fail("权限不足")
    try:
        item = DB_TableName_.get_by_id(data.id)
        DB_TableName_.delete(item)
        return Ret.success("删除成功")
    except Exception as e:
        logger.error(f"删除 {data} 资源时发生错误: {e}")
        return Ret.fail("删除失败")


logger.success(f"注册 {ROUTER_TAG} 路由表完成")
