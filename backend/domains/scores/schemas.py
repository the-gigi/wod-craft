from datetime import date, time, datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class BaseScore(BaseModel):
    class ConfigDict:
        from_attributes = True

    activity_id: int
    user_id: int
    when: str
    weight: Optional[int] = None
    reps: Optional[int] = None
    time: Optional[str] = None
    rx: bool = True  # as prescribed, no modifications
    dnf: bool = False  # did not finish
    notes: Optional[str] = None


class CreateScoreRequest(BaseScore):
    def dict(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data['when'] = str(self.when)
        if self.time:
            data['time'] = str(self.time)
        return data


class Score(BaseScore):
    id: int
