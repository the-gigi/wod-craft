from typing import List, Optional
from sqlmodel import Session, select
from .db_models import SQLActivity
from .schemas import Activity, CreateActivityRequest, ScoreType, Unit
import backend.db


class ActivityService:
    def __init__(self):
        """ """

    @property
    def engine(self):
        return backend.db.engine

    def _initialize_activities(self):
        initial_activities = [
            Activity(
                id=1,
                name="Bench press",
                description="5 x 135# bench press",
                weight=135,
                reps=5,
                time=None,
                unit=Unit.LB,
                score_type=ScoreType.WEIGHT.name
            ),
            Activity(
                id=2,
                name="Squat",
                description="5 x 225# squat",
                weight=225,
                reps=5,
                time=None,
                unit=Unit.LB,
                score_type=ScoreType.WEIGHT.name
            ),
            Activity(
                id=3,
                name="Deadlift",
                description="5 x 315# deadlift",
                weight=315,
                reps=5,
                time=None,
                unit=Unit.LB,
                score_type=ScoreType.WEIGHT.name
            )
        ]
        with Session(self.engine) as session:
            for activity in initial_activities:
                sql_activity = SQLActivity.model_validate(activity)
                session.add(sql_activity)
            session.commit()

    def get_activity(self, activity_id: int) -> Optional[Activity]:
        with Session(self.engine) as session:
            activity = session.get(SQLActivity, activity_id)
            return Activity.model_validate(activity) if activity else None

    def get_activities(self) -> List[Activity]:
        with Session(self.engine) as session:
            activities = session.exec(select(SQLActivity)).all()
            return [Activity.model_validate(activity) for activity in activities]

    def create_activity(self, activity: CreateActivityRequest) -> Activity:
        with Session(self.engine) as session:
            args = activity.model_dump()
            args.update(
                dict(score_type= activity.score_type if activity else None,
                     unit=activity.unit if activity.unit else None,
                     time=str(activity.time) if activity.time else None))
            new_activity = SQLActivity(**args)
            session.add(new_activity)
            try:
                session.commit()
            except Exception as e:
                raise ValueError(f"Activity with name {activity.name} already exists")
            session.refresh(new_activity)
            try:
                return Activity(id=new_activity.id, **args)
            except Exception as e:
                raise

    def update_activity(self, activity: Activity) -> Activity:
        with Session(self.engine) as session:
            existing_activity = session.get(SQLActivity, activity.id)
            if not existing_activity:
                raise ValueError(f"Activity with id {activity.id} does not exist")
            for key, value in activity.model_dump().items():
                setattr(existing_activity, key, value)
            session.add(existing_activity)
            session.commit()
            session.refresh(existing_activity)
            return activity

    def delete_activity(self, activity_id: int) -> None:
        with Session(self.engine) as session:
            activity = session.get(SQLActivity, activity_id)
            if not activity:
                raise ValueError(f"Activity with id {activity_id} does not exist")
            session.delete(activity)
            session.commit()
