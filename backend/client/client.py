import requests
from typing import List
from backend.domains.activities.schemas import Activity, CreateActivityRequest
from backend.domains.users.schemas import CreateUserRequest, User
from backend.domains.scores.schemas import Score, CreateScoreRequest


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def add_activity(self, activity: CreateActivityRequest) -> Activity:
        payload = activity.dict()
        response = requests.post(f"{self.base_url}/activities", json=payload)
        response.raise_for_status()
        return Activity.model_validate(response.json())

    def add_score(self, score: CreateScoreRequest) -> Score:
        url = f"{self.base_url}/scores"
        payload = score.dict()
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return Score.model_validate(response.json())

    def get_activities(self) -> List[Activity]:
        response = requests.get(f"{self.base_url}/activities")
        response.raise_for_status()
        return [Activity.model_validate(activity) for activity in response.json()]

    def get_activity(self, activity_id: int) -> Activity:
        response = requests.get(f"{self.base_url}/activities/{activity_id}")
        response.raise_for_status()
        return Activity.model_validate(response.json())

    def get_scores(self, user_id: int, activity_id: int) -> List[Score]:
        url = f"{self.base_url}/scores?user_id={user_id}&activity_id={activity_id}"
        response = requests.get(url)
        response.raise_for_status()
        return [Score.parse_obj(score) for score in response.json()]

    def add_user(self, user: CreateUserRequest) -> User:
        payload = user.model_dump()
        response = requests.post(f"{self.base_url}/users", json=payload)
        response.raise_for_status()
        return User.model_validate(response.json())

    def get_users(self) -> List[User]:
        response = requests.get(f"{self.base_url}/users")
        response.raise_for_status()
        return [User.model_validate(user) for user in response.json()]

    def get_user(self, name: str) -> User:
        response = requests.get(f"{self.base_url}/users/{name}")
        response.raise_for_status()
        return User.model_validate(response.json())

    def login(self, email: str) -> str:
        """ """
        response = requests.post(f"{self.base_url}/login", json={"email": email})
        response.raise_for_status()
        return response.json()["token"]

    def logout(self, token: str) -> str:
        """ """
        response = requests.post(f"{self.base_url}/logout", json={"token": token})
        response.raise_for_status()
        return response.json()["token"]
