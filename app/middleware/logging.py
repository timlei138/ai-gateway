# backend/middleware/logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..models.log import APICallLog
import time


class APIMetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/v1/chat"):
            return await call_next(request)

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        try:
            project = request.state.project
            await APICallLog.create(
                project=project,
                duration=duration,
                input_tokens=0,  # 需要实际解析
                output_tokens=0
            )
        except Exception as e:
            print(e)

        return response
