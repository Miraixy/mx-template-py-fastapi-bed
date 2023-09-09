import sys
from enum import Enum
from typing import Dict

from configs.config import Config, DevConfig, ProdConfig


class Env(Enum):
    Dev = "dev"
    Prod = "prod"


mapping: Dict[Env, Config] = {Env.Dev: DevConfig, Env.Prod: ProdConfig}  # type: ignore
# 获取运行参数中的环境参数 env=dev
APP_ENV: str = ""

for env in sys.argv[:]:
    if env.startswith("env="):
        env = env.split("=")[-1]
        APP_ENV = env
        break
else:
    # 默认为开发环境
    APP_ENV = Env.Dev # type: ignore

config: Config = mapping[APP_ENV]()  # type: ignore
