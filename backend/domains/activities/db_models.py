from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from .schemas import Activity, Score
from ..users.db_models import SQLUser


# SQLActivity inherits from the existing Pydantic Activity model
class SQLActivity(Activity, SQLModel, table=True):
    __tablename__ = "activities"
    id: int = Field(default=None, primary_key=True)


# SQLScore inherits from the existing Pydantic Score model
class SQLScore(Score, SQLModel, table=True):
    __tablename__ = "scores"
    id: int = Field(default=None, primary_key=True)

    # Foreign keys
    activity_id: int = Field(foreign_key="activities.id")
    user_id: int = Field(foreign_key="users.id")

    # Fields from the original Score schema
    weight: Optional[int] = None
    reps: Optional[int] = None
    time: Optional[int] = None
    rx: bool
    dnf: bool
    notes: Optional[str] = None

    # Relationships
    activity: SQLActivity = Relationship(cascade_delete=False)
    # user: SQLUser = Relationship(back_populates="scores")
