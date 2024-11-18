from datetime import date, time, datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from passlib.hash import bcrypt
ROLE_USER = 0
ROLE_ADMIN = 1

UNITS = {
    'LB': 'Pounds',
    'KG': 'Kilograms',
    'Pood': 'Pood'
}

SCORE_TYPES = {
    'Rounds': 'Complete as many rounds as possible',
    'Reps': 'Complete as many repetitions as possible',
    'Weight': 'Lift as much weight as possible',
    'Time': 'Complete as fast as possible'
}


class TagLinkScore(SQLModel, table=True):
    __tablename__ = "tags"
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    score_id: Optional[int] = Field(default=None, foreign_key="score.id", primary_key=True)


class Unit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=4, unique=True)
    description: str = Field(max_length=64)
    activities: List["Activity"] = Relationship(back_populates="unit")


class ScoreType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=10, unique=True)
    description: str = Field(max_length=64)
    activities: List["Activity"] = Relationship(back_populates="score_type")


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    score_type_id: int = Field(foreign_key="score_type.id", index=True)
    name: str = Field(max_length=256, unique=True)
    description: str = Field(max_length=4096, unique=True)
    weight: Optional[int] = None
    reps: Optional[int] = None
    time: Optional[datetime] = None

    unit: Optional[Unit] = Relationship(back_populates="activities")
    score_type: ScoreType = Relationship(back_populates="activities")
    scores: List["Score"] = Relationship(back_populates="activity")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=64, unique=True)
    email: str = Field(max_length=120, unique=True, index=True)
    password: str = Field(max_length=128)
    role: int = Field(default=ROLE_USER)

    scores: List["Score"] = Relationship(back_populates="user")
    tags: List["Tag"] = Relationship(back_populates="user")

    def hash_password(self, password: str) -> None:
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)


class Score(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    when: date
    weight: Optional[int] = None
    reps: Optional[int] = None
    time: Optional[time] = None
    rx: bool
    comments: Optional[str] = Field(default=None, max_length=256)

    user: User = Relationship(back_populates="scores")
    activity: Activity = Relationship(back_populates="scores")
    tags: List["Tag"] = Relationship(back_populates="scores", link_model=TagLinkScore)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    tag: str = Field(max_length=64)

    user: User = Relationship(back_populates="tags")
    scores: List[Score] = Relationship(back_populates="tags", link_model=TagLinkScore)

    class Config:
        table_args = ({"UniqueConstraint": ("user_id", "tag")},)
