import sys
from typing import Dict

from configs.config import Config, DevConfig, ProdConfig

mapping: Dict[str, Config] = {"dev": DevConfig, "prod": ProdConfig}  # type: ignore

# 获取运行参数中的环境参数 env=dev
APP_ENV: str = ""

for env in sys.argv[:]:
    if env.startswith("env="):
        env = env.split("=")[-1]
        APP_ENV = env
        break
else:
    # 默认为开发环境
    APP_ENV = "dev"

config: Config = mapping[APP_ENV]()  # type: ignore
