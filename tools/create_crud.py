import sys
from pathlib import Path
from time import sleep

TARGET_NAME: str = ""
AUTO_ADDITION: bool = False

for env in sys.argv[:]:
    if env.startswith("name="):
        env = env.split("=")[-1]
        TARGET_NAME = env
        break
else:
    raise Exception("缺少必须的 `name` 参数")

if "-a" in sys.argv:
    AUTO_ADDITION = True

OUTPUT_CLASS_NAME = "".join([i.capitalize() for i in TARGET_NAME.split("_")])
OUTPUT_LOWER_NAME = TARGET_NAME.lower().replace(" ", "_").replace("-", "_")
OUTPUT_CAPITAL_NAME = (
    TARGET_NAME[0].upper()
    + TARGET_NAME.lower().replace(" ", "_").replace("-", "_")[1:]
)

MODEL_TEMPLATE_PATH: str = "./src/models/template.py"
SCHEMA_TEMPLATE_PATH: str = "./src/schemas/template.py"
ROUTER_TEMPLATE_PATH: str = "./src/routers/template.py"

MODEL_OUTPUT_PATH: str = f"./src/models/{OUTPUT_LOWER_NAME}.py"
SCHEMA_OUTPUT_PATH: str = f"./src/schemas/{OUTPUT_LOWER_NAME}.py"
ROUTER_OUTPUT_PATH: str = f"./src/routers/{OUTPUT_LOWER_NAME}.py"

APP_PY_PATH: str = "./src/app.py"
MODEL_INIT_PY_PATH: str = "./src/models/__init__.py"


def content_replace(content: str) -> str:
    return (
        content.replace(
            "_TableName_",
            OUTPUT_CLASS_NAME,
        )
        .replace(
            "_Table_name_",
            OUTPUT_CAPITAL_NAME,
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


def append_line_before_anchor_text(
    original_text, anchor_text: str, new_line: str,
) -> str:
    if new_line in original_text:
        print(f"* WARNING: `{new_line}` 已经存在，跳过该行")
        return original_text
    return original_text.replace(anchor_text, f"{new_line}\n{anchor_text}")


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

    if AUTO_ADDITION:
        print(
            "自动追加已启用，将在 5s 后执行自动追加操作"
            "! 注意: 自动追加完成后如需撤销请手动删除追加的代码，请勿在 IED 中使用 Ctrl+Z 撤销操作，否则可能造成代码格式异常",
        )
        sleep(5)
        original_file_text = Path.open(Path(APP_PY_PATH), encoding="utf-8").read()
        app_file_text = append_line_before_anchor_text(
            original_file_text,
            "# $import_routers$",
            f"from src.routers.{OUTPUT_LOWER_NAME} import router as {OUTPUT_LOWER_NAME}_router",
        )
        app_file_text = append_line_before_anchor_text(
            app_file_text,
            "# $include_routers$",
            f'app.include_router({OUTPUT_LOWER_NAME}_router, prefix="/{OUTPUT_LOWER_NAME}", tags=["{OUTPUT_CAPITAL_NAME}"])',
        )
        with Path.open(Path(APP_PY_PATH), "w", encoding="utf-8") as f:
            f.write(app_file_text)

        original_file_text = Path.open(
            Path(MODEL_INIT_PY_PATH),
            encoding="utf-8",
        ).read()
        new_file_text = append_line_before_anchor_text(
            original_file_text,
            "# $table_create$",
            f"from src.models.{OUTPUT_LOWER_NAME} import DB{OUTPUT_CLASS_NAME}  # noqa: F401",
        )
        with Path.open(Path(MODEL_INIT_PY_PATH), "w", encoding="utf-8") as f:
            f.write(new_file_text)

        print(
            "CRUD 模板创建成功,请在 `src/models`、`src/routers` 和 `src/schemas` 目录下查看生成的文件\n",
            "* 自动追加：已在 `./src/app.py` 和 `./src/models/__init__.py` 中添加模板引入",
        )

    else:
        print(
            "CRUD 模板创建成功,请在 `src/models`、`src/routers` 和 `src/schemas` 目录下查看生成的文件\n\n"
            f"* 请在 `/src/models/__init__.py` 中使用 `from src.models.{OUTPUT_LOWER_NAME} import DB{OUTPUT_CLASS_NAME}` 导入生成的数据模型\n\n"
            "* 请在 `/src/app.py` 中使用\n"
            f"  > `from src.routers.{OUTPUT_LOWER_NAME} import router as {OUTPUT_LOWER_NAME}_router` 导入生成的路由\n"
            f'  > `app.include_router({OUTPUT_LOWER_NAME}_router, prefix="/{OUTPUT_LOWER_NAME}", tags=["{OUTPUT_CAPITAL_NAME}"])` 来注册路由\n',
        )
