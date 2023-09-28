# Python FastAPI Template

## 中文文档请查看 [README_zh.md](https://github.com/Miraixy/mx-template-py-fastapi-bed/blob/main/README_zh.md)

## Basic Features

- [x] Basic framework
- [x] Switchable environment configurations
- [x] Automatic code reloading
- [x] SQLAlchemy-based ORM
- [x] Swagger API documentation support
- [x] Logging using the logure framework
- [x] JWT authentication
- [x] RUFF code standards
- [x] One-line command to generate CRUD templates including model, schema, and router
- [x] Complete CI/CD workflow and production environment Docker-compose automatic deployment template
- [x] Using RUFF to standardize code

## Getting Started

### 1. Install Poetry

```bash
pip install poetry
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Start Development

```bash
poetry run app
```

### 4. Switch Environments

```bash
poetry run app env=dev  # Development environment (default)
poetry run app env=prod # Production environment
```

In `dev` environment, the development server will automatically reload the code

## Generate CRUD Templates (Automatically appends model creation and router inclusion) *RECOMMENDED*

> ! Note: After automatic appending, if you need to undo it, please manually delete the appended code. Do not use Ctrl+Z in the IDE, as it may cause code formatting issues.

### 1. Execute the following command

```bash
poetry run create_crud name={data_model_name} -a  # Use `_` as a separator for multi-word names, case-insensitive
```

For example:

```bash
poetry run create_crud name=example -a
```

## Generate CRUD Templates (Manually add model creation and router inclusion)

### 1. Execute the following command

```bash
poetry run create_crud name={data_model_name} -a  # Use `_` as a separator for multi-word names, case-insensitive
```

For example:

```bash
poetry run create_crud name=example
```

### 2. Add automatic table creation

In `src/models/__init__.py`, import your associated models under `# $table_create$`:

```python
# $table_create$ 自动创建表追加锚 *请不要修改此行* (Anchor of the table creation line *Do not modify this line*)
from .{data_model_name} import DB{DataModelClassName}
```

### 3. Mount the router

In `src/app.py`, under Mount the router tables, add the router:

```python
from src.routers.{data_model_name} import router as {data_model_name}_router

app.include_router({data_model_name}_router, prefix="/{router_prefix}", tags=["{router_tag}"])
```

Please replace `{data_model_name}`, `{DataModelClassName}`, `{router_prefix}`, and `{router_tag}` with the appropriate values as needed for your project.
