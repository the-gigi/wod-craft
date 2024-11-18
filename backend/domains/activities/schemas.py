from datetime import date, time, datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from enum import Enum


# from ..users.schemas import User


class Unit(Enum):
    LB = 'Pounds'
    KG = 'Kilograms'
    POOD = 'Pood'


class ScoreType(Enum):
    AMRAP = 'AMRAP'  # Complete as many rounds/reps as possible
    REPS = 'Reps'  # Complete as many repetitions as possible
    WEIGHT = 'Weight'  # Lift as much weight as possible
    TIME = 'Time'  # Complete as fast as possible
    EMOM = 'EMOM'  # Perform the activity every minute on the minute for the specified duration)
    FIXED = 'Fixed'  # Complete the activity as specified (e.g 5 reps of 05 pounds)


class BaseActivity(BaseModel):
    class ConfigDict:
        from_attributes = True
    name: str
    description: str
    weight: Optional[int] = None
    reps: Optional[int] = None
    time: Optional[timedelta] = None
    unit: Optional[Unit] = None
    score_type: ScoreType


class CreateActivityRequest(BaseActivity):
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data['score_type'] = self.score_type.value
        if self.unit:
            data['unit'] = self.unit.value
        if self.time:
            data['time'] = str(self.time)
        return data


class Activity(BaseActivity):
    id: int


class BaseScore(BaseModel):
    class ConfigDict:
        from_attributes = True

    activity_id: int
    user_id: int
    when: date
    weight: Optional[int] = None
    reps: Optional[int] = None
    time: Optional[time] = None
    rx: bool  # as prescribed, no modifications
    dnf: bool  # did not finish
    notes: Optional[str] = None


class CreateScoreRequest(BaseModel):
    """ """


class Score(BaseScore):
    id: int
