# Python FastAPI Template

## 基本功能

- [x] 基本框架
- [x] 可切换的环境配置
- [x] 基于 SQLAlchemy 的 ORM
- [x] Swagger 接口文档支持
- [x] 基于 logure 框架的日志记录
- [x] JWT 鉴权
- [x] RUFF 代码规范

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
