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
                format=settings.log.format_console,
                filter=lambda record: record["extra"].get("module") == module_name,
                level=settings.log.level,
                colorize=True,
                backtrace=True,
                diagnose=True,
            )

            os.makedirs(settings.log.dir, exist_ok=True)
            log_file = Path(settings.log.dir) / f"{module_name}.log"

            if settings.log.rotation_enabled:
                loguru_logger.add(
                    log_file,
                    format=settings.log.format_file,
                    filter=lambda record: record["extra"].get("module") == module_name,
                    level=settings.log.level,
                    rotation=settings.log.rotation,
                    retention=settings.log.retention,
                    compression=settings.log.compression,
                    colorize=True,
                    backtrace=True,
                    diagnose=True,
                )
            else:
                loguru_logger.add(
                    log_file,
                    format=settings.log.format_file,
                    filter=lambda record: record["extra"].get("module") == module_name,
                    level=settings.log.level,
                    colorize=True,
                    backtrace=True,
                    diagnose=True,
                )

            self._initialized_modules.add(module_name)

    def _get_caller_info(self):
        frame = None
        try:
            frame = inspect.currentframe()
            print(frame)

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

    def _get_logger_with_context(self):
        filename, line_no = self._get_caller_info()
        return loguru_logger.bind(
            filename=filename, line_no=line_no, module=self.module_name
        )

    def debug(self, msg: str, obj: Optional[Any] = None):
        filename, line_no = self._get_caller_info()
        log = self._get_logger_with_context()
        if obj is not None:
            log.debug(f"{msg} | {obj}")
        else:
            log.debug(msg)

    def info(self, msg: str, obj: Optional[Any] = None):
        filename, line_no = self._get_caller_info()
        log = self._get_logger_with_context()
        if obj is not None:
            log.info(f"{msg} | {obj}")
        else:
            log.info(msg)

    def error(self, msg: str, obj: Optional[Any] = None, exc_info=None):
        filename, line_no = self._get_caller_info()
        log = self._get_logger_with_context()
        message = f"{msg} | {obj}" if obj is not None else msg
        if exc_info:
            log.exception(message)
        else:
            log.error(message)

    def critical(self, msg: str, obj: Optional[Any] = None):
        filename, line_no = self._get_caller_info()
        log = self._get_logger_with_context()
        if obj is not None:
            log.critical(f"{msg} | {obj}")
        else:
            log.critical(msg)

    def warning(self, msg: str, obj: Optional[Any] = None):
        filename, line_no = self._get_caller_info()
        log = self._get_logger_with_context()
        if obj is not None:
            log.warning(f"{msg} | {obj}")
        else:
            log.warning(msg)

    def trace(self, msg: str, obj: Optional[Any] = None):
        filename, line_no = self._get_caller_info()
        log = self._get_logger_with_context()
        if obj is not None:
            log.trace(f"{msg} | {obj}")
        else:
            log.trace(msg)


def get_logger(module_name: str) -> Logger:
    return Logger(module_name)
