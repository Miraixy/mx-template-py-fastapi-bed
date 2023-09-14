# 使用 Python 官方镜像作为基础镜像
FROM python:3.8.0

# 安装 Poetry
RUN pip install poetry

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 安装项目依赖项
RUN poetry install

# 启动应用
CMD ["poetry", "run", "app", "env=prod"]
