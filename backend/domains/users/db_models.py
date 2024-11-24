from __future__ import annotations
from sqlmodel import Field, SQLModel, Relationship
from .schemas import User, Role


class SQLUser(User, SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    role: Role = Field(default=Role.USER)

    # Establish a relationship with tags
    #tags: list["SQLTag"] = Relationship(back_populates="user")


class SQLTag(SQLModel, table=True):
    __tablename__ = "tags"
    id: int | None  = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    tag: str

    # Define a relationship to the SQLUser model
    #user: SQLUser | None = Relationship(back_populates="tags")