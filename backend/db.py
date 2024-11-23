import os
from typing import Optional

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.engine.base import Engine
from dotenv import load_dotenv

engine: Optional[AsyncEngine | Engine] = None
DATABASE_TYPE = "sqlite"
SQLITE_FILENAME = "wodcraft.db"
SQLITE_URL = ""
POSTGRES_URL = ""


def init_db():
    global engine
    global DATABASE_TYPE
    global SQLITE_FILENAME
    global SQLITE_URL
    global POSTGRES_URL

    # Get the database type from environment variables
    DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")

    # Set up database URLs
    SQLITE_FILENAME = os.getenv("SQLITE_FILENAME", "wodcraft.db")
    SQLITE_URL = f"sqlite:///{SQLITE_FILENAME}"
    POSTGRES_URL = os.getenv("POSTGRES_URL")

    # Set up the engine based on the selected database type
    if DATABASE_TYPE == "postgres":
        engine = create_async_engine(POSTGRES_URL, echo=True)
    else:
        connect_args = {"check_same_thread": False}
        engine = create_engine(SQLITE_URL, connect_args=connect_args, echo=True)


# Function to create database tables

async def create_db_and_tables():
    init_db()

    print(f"Creating tables for {DATABASE_TYPE} database...")
    if DATABASE_TYPE == "postgres":
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    else:
        print("Using SQLite engine")
        SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")
