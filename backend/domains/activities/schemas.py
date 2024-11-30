from datetime import date, time, datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Unit(Enum):
    POUNDS = 'Pounds'
    KILOGRAMS = 'Kilograms'
    POOD = 'Pood'


class ScoreType(Enum):
    AMRAP = 'AMRAP'  # Complete as many rounds/reps as possible
    REPS = 'Reps'  # Complete as many repetitions as possible
    WEIGHT = 'Weight'  # Lift as much weight as possible
    TIME = 'Time'  # Complete as fast as possible
    EMOM = 'EMOM'  # Perform the activity every minute on the minute for the specified duration)
    DEATH_BY_X = 'Death by X'  # Perform the activity every minute on the minute, increasing the number of reps by 1 each minute until failure, the score is the number of minutes
    TABATA = 'Tabata'  # Perform each of the 4 activities for 20 seconds, rest for 10 seconds, repeat 8 times, the score for each activity is the lowest number of reps in a round
    FIXED = 'Fixed'  # Complete the activity as specified (e.g 5 reps of 05 pounds)


class BaseActivity(BaseModel):
    class Config:
        from_attributes = True

    def dict(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data['score_type'] = self.score_type
        if self.unit:
            data['unit'] = self.unit
        if self.time:
            data['time'] = str(self.time)
        data['children'] = [
            sa.dict() for sa in self.children] if self.sub_activities else None
        return data

    name: str
    description: str
    weight: Optional[int] = None
    reps: Optional[int] = None
    time: Optional[timedelta] = None
    unit: Optional[str] = None
    score_type: str


class CreateActivityRequest(BaseActivity):
    sub_activities: Optional[list[int]] = None


class Activity(BaseActivity):
    id: int
    parent_id: Optional[int] = None # parent activity id


