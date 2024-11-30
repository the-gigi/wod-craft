from typing import List, Optional
from sqlmodel import Session, select
from .db_models import SQLScore
from .schemas import Score, CreateScoreRequest
import backend.db


class ScoreService:
    @property
    def engine(self):
        return backend.db.engine

    def get_score(self, score_id: int) -> Optional[Score]:
        with Session(self.engine) as session:
            score = session.get(SQLScore, score_id)
            return Score.model_validate(score) if score else None

    def get_scores(self, user_id: int, activity_id: int) -> List[Score]:
        with Session(self.engine) as session:
            query = select(SQLScore)
            if user_id:
                query = query.where(SQLScore.user_id == user_id)
            if activity_id:
                query = query.where(SQLScore.activity_id == activity_id)

            scores = session.exec(query).all()
            return [Score.model_validate(score) for score in scores]

    def create_score(self, score: CreateScoreRequest) -> Score:
        with Session(self.engine) as session:
            args = score.model_dump()
            args.update(
                dict(when=str(score.when) if score.when else None,
                     time=str(score.time) if score.time else None))
            new_score = SQLScore(**args)
            session.add(new_score)
            try:
                session.commit()
            except Exception as e:
                session.commit()
            session.refresh(new_score)
            try:
                return Score(id=new_score.id, **args)
            except Exception as e:
                raise

    def update_score(self, score_id, score: Score) -> Score:
        with Session(self.engine) as session:
            existing_score = session.get(SQLScore, score_id)
            if not existing_score:
                raise ValueError(f"Score with id {score_id} does not exist")
            for key, value in score.model_dump().items():
                setattr(existing_score, key, value)
            session.add(existing_score)
            session.commit()
            session.refresh(existing_score)
            return score

    def delete_score(self, score_id: int) -> None:
        with Session(self.engine) as session:
            score = session.get(SQLScore, score_id)
            if not score:
                raise ValueError(f"Score with id {score_id} does not exist")
            session.delete(score)
            session.commit()
