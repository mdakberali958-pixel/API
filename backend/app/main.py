from collections import defaultdict
from time import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.core.config import settings
from backend.app.api.routes import chat, auth, admin, kb, eval

app = FastAPI(title=settings.app_name, version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_request_buckets: dict[str, list[float]] = defaultdict(list)


@app.middleware("http")
async def simple_rate_limiter(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    now = time()
    window_start = now - 60
    _request_buckets[client_ip] = [t for t in _request_buckets[client_ip] if t >= window_start]

    if len(_request_buckets[client_ip]) >= settings.rate_limit_per_minute:
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

    _request_buckets[client_ip].append(now)
    return await call_next(request)


app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(chat.router, prefix=settings.api_v1_prefix)
app.include_router(admin.router, prefix=settings.api_v1_prefix)
app.include_router(kb.router, prefix=settings.api_v1_prefix)
app.include_router(eval.router, prefix=settings.api_v1_prefix)


@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name, "version": app.version}
