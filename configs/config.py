from typing import Literal


class Config:
    """Configuration"""

    def __getitem__(self, key):
        return self.__getattribute__(key)

    HOST: str = "0.0.0.0"
    PORT: int = 8090
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    UVICORN_LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "WARNING"
    DATABASE_URL: str = "sqlite:///./test.sqlite3.db"
    JWT_SECRET_KEY: str = "secret:Miraixy-TEMPLATE"
    JWT_REFRESH_SECRET_KEY: str = "refresh:Miraixy-TEMPLATE"
    SUPER_ACCESS_KEY: str = "Miraixy-TEMPLATE"
    RELOAD: bool = False
    DEBUG: bool = True
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7


class DevConfig(Config):
    """Development environment configuration"""

    LOG_LEVEL = "DEBUG"
    UVICORN_LOG_LEVEL = "DEBUG"
    DATABASE_URL = "sqlite:///./test.sqlite3.db"
    RELOAD = True
    DEBUG = True


class ProdConfig(Config):
    """Production environment configuration"""

    LOG_LEVEL = "WARNING"
    UVICORN_LOG_LEVEL = "WARNING"
    DEBUG = False
