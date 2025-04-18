import inspect
import os
import sys
from pathlib import Path
from typing import Any, Optional

from loguru import logger as loguru_logger

from app.core.config import settings

loguru_logger.remove()


class Logger:
    _initialized_modules = set()

    def __init__(self, module_name: str):
        self.module_name = module_name
        self.logger = loguru_logger.bind(module=module_name)

        if module_name not in self._initialized_modules:
            loguru_logger.add(
                sys.stdout,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[filename]}</cyan>:<cyan>{extra[line_no]}</cyan> - <level>{message}</level>",
                filter=lambda record: record["extra"].get("module") == module_name,
                level=settings.LOG_LEVEL,
                colorize=True,
                backtrace=True,
                diagnose=True,
            )

            os.makedirs(settings.LOG_DIR, exist_ok=True)
            log_file = Path(settings.LOG_DIR) / f"{module_name}.log"

            if settings.LOG_ROTATION:
                loguru_logger.add(
                    log_file,
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[filename]}:{extra[line_no]} - {message}",
                    filter=lambda record: record["extra"].get("module") == module_name,
                    level=settings.LOG_LEVEL,
                    rotation="10 MB",
                    retention="1 week",
                    compression="zip",
                    backtrace=True,
                    diagnose=True,
                )
            else:
                loguru_logger.add(
                    log_file,
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[filename]}:{extra[line_no]} - {message}",
                    filter=lambda record: record["extra"].get("module") == module_name,
                    level=settings.LOG_LEVEL,
                    backtrace=True,
                    diagnose=True,
                )

            self._initialized_modules.add(module_name)

    def _get_caller_info(self):
        frame = None
        try:
            frame = inspect.currentframe()

            for _ in range(3):
                if not frame or not frame.f_back:
                    return "Unknown", 0
                frame = frame.f_back
            full_path = getattr(frame.f_code, "co_filename", None)
            if not full_path:
                return "unknown", 0

            parts = Path(full_path).parts
            filepath = (
                os.path.join(*parts[-3:]) if len(parts) >= 3 else os.path.join(*parts)
            )
            return filepath, frame.f_lineno
        except Exception:
            return "unknown", 0
        finally:
            if frame:
                del frame

    def debug(self, msg: str, obj: Optional[Any] = None):
        filename, line_no = self._get_caller_info()
        log = self.logger.bind(filename=filename, line_no=line_no)
        if obj is not None:
            log.debug(f"{msg} | {obj}")
        else:
            log.debug(msg)

    def info(self, msg: str, obj: Optional[Any] = None):
        filename, line_no = self._get_caller_info()
        log = self.logger.bind(filename=filename, line_no=line_no)
        if obj is not None:
            log.info(f"{msg} | {obj}")
        else:
            log.info(msg)

    def error(self, msg: str, obj: Optional[Any] = None, exc_info=None):
        filename, line_no = self._get_caller_info()
        log = self.logger.bind(filename=filename, line_no=line_no)
        message = f"{msg} | {obj}" if obj is not None else msg
        if exc_info:
            log.exception(message)
        else:
            log.error(message)

    def critical(self, msg: str, obj: Optional[Any] = None):
        filename, line_no = self._get_caller_info()
        log = self.logger.bind(filename=filename, line_no=line_no)
        if obj is not None:
            log.critical(f"{msg} | {obj}")
        else:
            log.critical(msg)


def get_logger(module_name: str) -> Logger:
    return Logger(module_name)
