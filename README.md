# Python FastAPI Template

## 基本功能

- [x] 基本框架
- [x] 可切换的环境配置
- [x] 基于 SQLAlchemy 的 ORM
- [x] Swagger 接口文档支持
- [x] 基于 logure 框架的日志记录
- [x] JWT 鉴权
- [x] RUFF 代码规范
- [x] 一行命令生成包括 model, schema, router 的 CRUD 模板
- [x] 完整的 CI/CD 流程和生产环境 Docker-compose 自动部署模板

## 启动开发

### 1. 安装 Poetry

```bash
pip install poetry
```

### 2. 安装依赖

```bash
poetry install
```

### 3. 启动开发

```bash
poetry run app
```

### 4. 切换环境

```bash
poetry run app env=dev  # 开发环境 (default)
poetry run app env=prod # 生产环境
```

## 生成 CRUD 模板 (自动追加模型创建、路由引入)
> ! 注意: 自动追加完成后如需撤销请手动删除追加的代码，请勿在 IED 中使用 Ctrl+Z 撤销操作，否则可能造成代码格式异常

### 1. 执行以下命令

```bash
poetry run create_crud name={数据模型名} -a  # 多词使用 `_` 作为分隔 大小写不敏感

```
例如:

```bash
poetry run create_crud name=example
```

## 生成 CRUD 模板 (手动添加模型创建、路由引入)

### 1. 执行以下命令

```bash
poetry run create_crud name={数据模型名}  # 多词使用 `_` 作为分隔 大小写不敏感
```

### 2. 添加数据表自动创建

在 `src/models/__init__.py` 的 `引入所有需要自动创建的表模型` 引入你的关联模型:

```python
# TODO 引入所有需要自动创建的表模型
from .{数据模型名} import DB{数据模型类名}  # 数据模型类名为数据模型名的大驼峰形式 例如: UserData
```

### 3. 挂载路由

在 `src/app.py` 中的 `挂载路由表` 添加路由:

```python
from src.routers.{数据模型名} import router as {数据模型名}_router

app.include_router({数据模型名}, prefix="/{路由前缀}", tags=["{路由标签}"])
```
