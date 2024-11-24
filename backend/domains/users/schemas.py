from enum import Enum
from pydantic import BaseModel, EmailStr


class Role(Enum):
    USER = 0
    ADMIN = 1


# Define the User models
class BaseUser(BaseModel):
    class ConfigDict:
        from_attributes = True

    name: str
    email: str


class CreateUserRequest(BaseUser):
    """ """


class User(BaseUser):
    id: int
    role: Role
    token: str | None


class Tag(BaseModel):
    class ConfigDict:
        from_attributes = True

    user_id: int
    tag: str
