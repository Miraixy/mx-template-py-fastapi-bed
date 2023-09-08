import logging
import sys
from typing import TYPE_CHECKING, Any, Callable, TextIO, Union

from loguru import logger as logger

from src.conf import config

if TYPE_CHECKING:
    from logging import Handler

    from loguru import Message as LoguruMessage
    from loguru import Record as LoguruRecord
    from loguru import Writable


DEFAULT_FORMAT = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    # "<c>{function}:{line}</c>| "
    "{message}"
)


def abstract_filter(error_no: int) -> bool:
    config_level = config.LOG_LEVEL
    config_no = (
        logger.level(config_level).no if isinstance(config_level, str) else config_level
    )
    return error_no >= config_no


def default_filter(record: "LoguruRecord"):
    return abstract_filter(record["level"].no)


class LoguruHandler(logging.Handler):
    """logging 与 loguru 之间的桥梁，将 logging 的日志转发到 loguru。"""

    def emit(self, record: logging.LogRecord):
        level_no = record.levelno
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = level_no

        if not abstract_filter(level_no):
            return

        frame, depth = sys._getframe(6), 6  # noqa: SLF001
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def add_handler(
    handler: Union[TextIO, "Writable", Callable[["LoguruMessage"], Any], "Handler"],
    **kwargs,
) -> int:
    return logger.add(
        handler,
        level=0,
        diagnose=False,
        filter=default_filter,
        format=DEFAULT_FORMAT,
        **kwargs,
    )


def get_logging_config():
    uvicorn_lvl = config.UVICORN_LOG_LEVEL
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "default": {
                "class": "src.log.LoguruHandler",
            },
        },
        "loggers": {
            "uvicorn.error": {
                "handlers": ["default"],
                "level": uvicorn_lvl,
            },
            "uvicorn.access": {
                "handlers": ["default"],
                "level": uvicorn_lvl,
            },
        },
    }


def configure_logger():
    logger.remove()
    add_handler(sys.stdout)
