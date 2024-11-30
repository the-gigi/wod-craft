from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from .schemas import Activity


class SQLActivity(SQLModel, Activity, table=True):  # Inherit from Activity and SQLModel
    __tablename__ = "activities"
    id: int = Field(primary_key=True)
    parent_id: Optional[int] = Field(
        default=None,
        nullable=True,
        foreign_key="activities.id")
    parent: Optional['SQLActivity'] = Relationship(
      back_populates='children',
      sa_relationship_kwargs=dict(
        remote_side='SQLActivity.id'
      )
    )

    children: list['SQLActivity'] = Relationship(back_populates='parent')

    # name: str
    # description: str
    # weight: Optional[int] = None
    # reps: Optional[int] = None
    # time: Optional[int] = None
    # unit: Optional[str] = None
    # score_type: str

