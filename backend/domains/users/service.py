from typing import Dict
from .schemas import User, Role, CreateUserRequest, BaseUser


class UserService:
    def __init__(self):

        self.users: Dict[str, User] = {
            "the.gigi@gmail.com": User(
                id=1,
                name="Gigi",
                email="the.gigi@gmail.com",
                role=Role.ADMIN
            ),
            "guysayfan@gmail.com": User(
                id=2,
                name="Guy",
                email="guysayfan@gmail.com",
                role=Role.USER
            ),
            "lsayfan@gmail.com": User(
                id=3,
                name="Guy",
                email="lsayfan@gmail.com",
                role=Role.USER
            )
        }

    def get_user(self, email: str) -> User:
        return self.users.get(email)

    def get_users(self) -> Dict[str, User]:
        return self.users

    def create_user(self, user: CreateUserRequest) -> BaseUser:
        if user.email in self.users:
            raise ValueError(f"User with email {user.email} already exists")
        self.users[user.email] = User(
            id=len(self.users) + 1,
            name=user.name,
            email=user.email,
            role=Role.USER
        )
        return self.users[user.email]
