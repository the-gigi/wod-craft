
from sqlmodel import Field, SQLModel, Relationship, Column
from .schemas import Score
from ..activities.db_models import SQLActivity
from ..users.db_models import SQLUser


# SQLScore inherits from the existing Pydantic Score model
class SQLScore(Score, SQLModel, table=True):
    __tablename__ = "scores"
    id: int = Field(default=None, primary_key=True)

    # Foreign keys
    activity_id: int = Field(foreign_key="activities.id")
    user_id: int = Field(foreign_key="users.id")

    # Relationships
    activity: SQLActivity = Relationship(cascade_delete=False)
    user: SQLUser = Relationship(cascade_delete=False)
