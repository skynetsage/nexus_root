# from datetime import datetime
# from zoneinfo import ZoneInfo
#
# from fastapi import Request, UploadFile
# from starlette.middleware.base import BaseHTTPMiddleware
# import json
# from typing import Any, Union, Dict
#
# from ..config.logger import get_logger
#
# logger = get_logger("http")
#
# SENSITIVE_FIELDS = {"password", "secret", "token", "authorization", "api_key"}
#
#
# class RequestResponseLogger:
#     @staticmethod
#     def redact(data: Any) -> Any:
#         if isinstance(data, dict):
#             return {
#                 k: "********" if k.lower() in SENSITIVE_FIELDS
#                 else RequestResponseLogger.redact(v)
#                 for k, v in data.items()
#             }
#         return data
#
#     @staticmethod
#     async def get_body(request: Request) -> Union[Dict, str, None]:
#         content_type = request.headers.get('content-type', '')
#
#         if 'multipart/form-data' in content_type:
#             form = await request.form()
#             return {
#                 "form_fields": {
#                     k: "<file>" if isinstance(v, UploadFile) else str(v)
#                     for k, v in form.items()
#                 }
#             }
#
#         body = await request.body()
#         if not body:
#             return None
#
#         try:
#             json_body = json.loads(body)
#             return RequestResponseLogger.redact(json_body)
#         except json.JSONDecodeError:
#             return body.decode('utf-8', errors='replace')[:500]
#
#     @staticmethod
#     async def log(request: Request, response=None, duration=None):
#         body = await RequestResponseLogger.get_body(request)
#         log_data = {
#             "method": request.method,
#             "path": request.url.path,
#             "status": response.status_code if response else None,
#             "ms": round(duration * 1000, 2) if duration else None,
#             "body": body
#         }
#         logger.info(json.dumps(log_data))
#
#
# class LoggingMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         start = datetime.now(ZoneInfo("Asia/Kolkata"))
#
#         await RequestResponseLogger.log(request)
#
#         response = await call_next(request)
#
#         duration = (datetime.now(ZoneInfo("Asia/Kolkata")) - start).total_seconds()
#
#         await RequestResponseLogger.log(request, response, duration)
#
#         return response