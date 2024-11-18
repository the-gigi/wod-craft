import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import create_db_and_tables
from backend.deps import deps
from backend.internal import admin
from backend.domains import items
from backend.domains.users.routes import router as users_router
from backend.domains.activities.routes import router as activities_router
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(the_app: FastAPI):
    """ """
    # Perform startup tasks
    await create_db_and_tables()
    yield
    # Perform shutdown tasks if necessary


app = FastAPI(lifespan=lifespan)

app.include_router(items.router)
app.include_router(users_router)
app.include_router(activities_router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(deps.get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/healthz")
async def health_check():
    return {"status": "ok"}


def main():
    port = int(os.environ.get('PORT', 8000))

    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
