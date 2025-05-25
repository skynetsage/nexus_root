# import sys
# from typing import Dict
# from loguru import logger
# from pydantic_settings import BaseSettings
# from ..utils.config_util import load_yaml_config, PROJECT_ROOT
#
# class LoggingConfig(BaseSettings):
#     console_level: str
#     file_level: str
#     format: str
#     rotation: str
#     retention: str
#     compression: str
#     paths: Dict[str, str]
#
# def load_logging_config() -> LoggingConfig:
#
#     config = load_yaml_config("logging_config.yml")
#     return LoggingConfig(**config["logging"])
#
# def get_logger(module_name: str):
#     config = load_logging_config()
#
#     log_dir = PROJECT_ROOT / "logs"
#     log_dir.mkdir(exist_ok=True)
#
#     logger.remove()
#
#     if module_name in config.paths:
#         log_file_path = str((log_dir / config.paths[module_name]).resolve())
#         logger.add(
#             log_file_path,
#             level=config.file_level,
#             format=config.format,
#             rotation=config.rotation,
#             retention=config.retention,
#             compression=config.compression,
#             filter=lambda record: record["extra"].get("module") == module_name
#         )
#
#     logger.add(
#         sys.stderr,
#         level=config.console_level,
#         format=config.format,
#         backtrace=True,
#         diagnose=True,
#         enqueue=True
#     )
#
#     return logger.bind(module=module_name)
#
# def configure_sql_logs():
#
#     import logging
#     from sqlalchemy.engine import Engine
#     from sqlalchemy import event
#
#     logging.getLogger('sqlalchemy.engine').handlers = []
#
#     @event.listens_for(Engine, "before_cursor_execute")
#     def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#
#         module = "core"
#         log = get_logger(module)
#         log.debug(
#             "SQL Query:\n" + statement +
#             f"\nParameters: {parameters}" if parameters else ""
#         )
#
#     @event.listens_for(Engine, "after_cursor_execute")
#     def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#         pass
