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
    email: EmailStr


class CreateUserRequest(BaseUser):
    """ """


class User(BaseUser):
    role: Role


class Tag(BaseModel):
    class ConfigDict:
        from_attributes = True

    user_id: int
    tag: str
