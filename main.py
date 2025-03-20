from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.database.database import init_db, init_default_admin
from app.routers import auth, projects, ai, admin
from app.config.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.example.com"] if settings.ENV == "prod" else ["*"]
)

app.add_middleware(GZipMiddleware)


@asynccontextmanager
async def lifespan():
    print("lifespan.....")
    await init_db(settings)
    await init_default_admin()

init_db(settings)
init_default_admin()

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(ai.router)
app.include_router(admin.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
