import requests
from typing import List
from backend.domains.activities.schemas import Activity, CreateActivityRequest, Score


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def add_activity(self, activity: CreateActivityRequest) -> Activity:
        payload = activity.dict()
        response = requests.post(f"{self.base_url}/activities", json=payload)
        response.raise_for_status()
        return Activity.model_validate(response.json())

    def add_score(self, activity_id: int, score: Score) -> Score:
        response = requests.post(f"{self.base_url}/activities/{activity_id}/scores",
                                 json=score.dict())
        response.raise_for_status()
        return Score.parse_obj(response.json())

    def get_activities(self) -> List[Activity]:
        response = requests.get(f"{self.base_url}/activities")
        response.raise_for_status()
        return [Activity.model_validate(activity) for activity in response.json()]

    def get_scores(self, activity_id: int) -> List[Score]:
        response = requests.get(f"{self.base_url}/activities/{activity_id}/scores")
        response.raise_for_status()
        return [Score.parse_obj(score) for score in response.json()]
