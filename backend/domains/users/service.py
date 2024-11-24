import random
from typing import Dict

from .db_models import SQLUser
from .schemas import User, Role, CreateUserRequest, BaseUser

from typing import List, Optional
from sqlmodel import Session, select
from sqlmodel.sql.expression import Select, SelectOfScalar
import backend.db
from ..activities.db_models import SQLActivity


class UserService:
    def __init__(self):
        """ """
        # self.users: Dict[str, User] = {
        #     "the.gigi@gmail.com": User(
        #         id=1,
        #         name="Gigi",
        #         email="the.gigi@gmail.com",
        #         role=Role.ADMIN
        #     ),
        #     "guysayfan@gmail.com": User(
        #         id=2,
        #         name="Guy",
        #         email="guysayfan@gmail.com",
        #         role=Role.USER
        #     ),
        #     "lsayfan@gmail.com": User(
        #         id=3,
        #         name="Guy",
        #         email="lsayfan@gmail.com",
        #         role=Role.USER
        #     )
        # }

    @property
    def engine(self):
        return backend.db.engine

    def get_user(self, name: str) -> User:
        with Session(self.engine) as session:
            query = SelectOfScalar(SQLUser).where(SQLUser.name == name)
            user = session.exec(query)
            try:
                result = User.model_validate(user.one()) if user else None
                return result
            except Exception as e:
                raise ValueError(f"User with name {name} not found")

    def get_users(self) -> Dict[str, User]:
        # return self.users
        with Session(self.engine) as session:
            users = session.exec(select(SQLUser)).all()
            return {str(user.email): User.model_validate(user) for user in users}

    def create_user(self, user: CreateUserRequest) -> BaseUser:
        # if user.email in self.users:
        #     raise ValueError(f"User with email {user.email} already exists")
        # self.users[user.email] = SQLUser(
        #     id=len(self.users) + 1,
        #     name=user.name,
        #     email=user.email,
        #     role=Role.USER
        # )
        # return self.users[user.email]
        with Session(self.engine) as session:
            args = user.model_dump()
            args['email'] = str(user.email)
            new_user = SQLUser(**args)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return User(**new_user.model_dump())

    def login(self, email: str) -> str:
        """Generate random token and return it"""
        random.randbytes(16)
        with Session(self.engine) as session:
            query = SelectOfScalar(SQLUser).where(SQLUser.email == email)
            user = session.exec(query)
            user.token = random.randbytes(16)
            session.commit()
            return str(user.token)

    def logout(self, token) -> None:
        """ """
        with Session(self.engine) as session:
            query = SelectOfScalar(SQLUser).where(SQLUser.token == token)
            user = session.exec(query)
            user.token = None
            session.commit()
