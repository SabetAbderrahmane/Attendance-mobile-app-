from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.attendance import router as attendance_router
from app.api.routes.auth import router as auth_router
from app.api.routes.events import router as events_router
from app.api.routes.health import router as health_router
from app.api.routes.users import router as users_router
from app.core.config import get_settings
from app.db.init_db import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(users_router, prefix=settings.api_v1_prefix)
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(events_router, prefix=settings.api_v1_prefix)
app.include_router(attendance_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["root"], summary="Root endpoint")
def root() -> dict[str, str]:
    return {
        "message": f"{settings.app_name} is running",
        "environment": settings.app_env,
    }
