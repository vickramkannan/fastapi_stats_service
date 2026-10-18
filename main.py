import os
import time
import uuid
from typing import Callable, Awaitable

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

EMAIL = os.getenv("USER_EMAIL", "22f3000616@ds.study.iitm.ac.in")
ALLOWED_ORIGIN = "https://dash-8yzo4n.example.com"

api = FastAPI(title="Descriptive Statistics API")

# Strictly allow only the assigned origin. No wildcard origins.
api.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)

@api.get("/stats")
async def stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        numbers = [int(part.strip()) for part in values.split(",")]
        if not numbers or any(part.strip() == "" for part in values.split(",")):
            raise ValueError
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="values must be a comma-separated list of integers")

    total = sum(numbers)
    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }

class RequestMetadataMiddleware:
    """Adds request ID and elapsed processing time to every response, including preflights."""
    def __init__(self, app: Callable):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        started = time.perf_counter()

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                elapsed = max(0.0, time.perf_counter() - started)
                headers = list(message.get("headers", []))
                headers.append((b"x-request-id", request_id.encode("ascii")))
                headers.append((b"x-process-time", f"{elapsed:.6f}".encode("ascii")))
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_headers)

# Wrap the whole app so metadata headers are also added to CORS preflight responses.
app = RequestMetadataMiddleware(api)
