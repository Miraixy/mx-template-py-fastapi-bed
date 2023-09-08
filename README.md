# Python FastAPI Template

## 基本功能

[X] 基本框架
[X] 可切换的环境配置
[X] 基于 SQLAlchemy 的 ORM
[X] Swagger 接口文档支持
[X] 基于 logure 框架的日志记录
[X] JWT 鉴权
[X] RUFF 代码规范

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
poetry run app env=dev  # 开发环境(default)
poetry run app env=prod # 生产环境
```
