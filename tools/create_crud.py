import sys
from pathlib import Path

TARGET_NAME: str = ""

for env in sys.argv[:]:
    if env.startswith("name="):
        env = env.split("=")[-1]
        TARGET_NAME = env
        break
else:
    raise Exception("缺少必须的 `name` 参数")

OUTPUT_CLASS_NAME = "".join([i.capitalize() for i in TARGET_NAME.split("_")])
OUTPUT_LOWER_NAME = TARGET_NAME.lower().replace(" ", "_").replace("-", "_")

MODEL_TEMPLATE_PATH: str = "./src/models/template.py"
SCHEMA_TEMPLATE_PATH: str = "./src/schemas/template.py"
ROUTER_TEMPLATE_PATH: str = "./src/routers/template.py"

MODEL_OUTPUT_PATH: str = f"./src/models/{OUTPUT_LOWER_NAME}.py"
SCHEMA_OUTPUT_PATH: str = f"./src/schemas/{OUTPUT_LOWER_NAME}.py"
ROUTER_OUTPUT_PATH: str = f"./src/routers/{OUTPUT_LOWER_NAME}.py"


def content_replace(content: str) -> str:
    return (
        content.replace(
            "_TableName_",
            OUTPUT_CLASS_NAME,
        )
        .replace(
            "_table_name_",
            OUTPUT_LOWER_NAME,
        )
        .replace(
            "from src.schemas.template import",
            f"from src.schemas.{OUTPUT_LOWER_NAME} import",
        )
        .replace(
            "from src.models.template import",
            f"from src.models.{OUTPUT_LOWER_NAME} import",
        )
    )


def main():
    model_template = Path.open(Path(MODEL_TEMPLATE_PATH), encoding="utf-8").read()
    schema_template = Path.open(Path(SCHEMA_TEMPLATE_PATH), encoding="utf-8").read()
    router_template = Path.open(Path(ROUTER_TEMPLATE_PATH), encoding="utf-8").read()

    for output_path in [MODEL_OUTPUT_PATH, SCHEMA_OUTPUT_PATH, ROUTER_OUTPUT_PATH]:
        if Path.exists(Path(output_path)):
            print(f"* WARNING: 文件 {output_path} 已经存在，正在退出...")
            return

    with Path.open(Path(MODEL_OUTPUT_PATH), "w", encoding="utf-8") as f:
        f.write(content_replace(model_template))

    with Path.open(Path(SCHEMA_OUTPUT_PATH), "w", encoding="utf-8") as f:
        f.write(content_replace(schema_template))

    with Path.open(Path(ROUTER_OUTPUT_PATH), "w", encoding="utf-8") as f:
        f.write(content_replace(router_template))

    print(
        "CRUD 模板创建成功,请在 `src/models`、`src/routers` 和 `src/schemas` 目录下查看生成的文件\n\n"
        f"* 请在 `/src/models/__init__.py` 中使用 `from .{OUTPUT_LOWER_NAME} import DB{OUTPUT_CLASS_NAME}` 导入生成的数据模型\n\n"
        "* 请在 `/src/app.py` 中使用\n"
        f'  > `from src.routers.{OUTPUT_LOWER_NAME} import router as {OUTPUT_LOWER_NAME}_router` 导入生成的路由\n'
        f'  > `app.include_router({OUTPUT_LOWER_NAME}_router, prefix="/{OUTPUT_LOWER_NAME}", tags=["{OUTPUT_LOWER_NAME}"])` 来注册路由\n',
    )
