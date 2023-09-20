import sys
from enum import Enum
from typing import Dict, Type

from configs.config import Config, DevConfig, ProdConfig


class Env(Enum):
    Dev = "dev"
    Prod = "prod"
    Default = "dev"  # noqa: PIE796


mapping: Dict[str, Type[Config]] = {"dev": DevConfig, "prod": ProdConfig}
# 获取运行参数中的环境参数 env=dev
APP_ENV: Env = Env.Default

# Parse the command-line arguments
for arg in sys.argv[1:]:
    if arg.startswith("env="):
        env = arg.split("=")[-1]
        APP_ENV = Env(env)

# Use the updated APP_ENV value to retrieve the config
config: Config = mapping[APP_ENV.value]()