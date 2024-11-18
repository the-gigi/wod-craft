from fastapi import APIRouter

from .schemas import CreateUserRequest
from .service import UserService

router = APIRouter()
service = UserService()


@router.get("/users/", tags=["users"])
async def get_users():
    return service.get_users()


@router.get("/users/{email}", tags=["users"])
async def get_user(email: str):
    return service.get_user(email)


@router.post("/users/", tags=["users"])
async def create_user(user: CreateUserRequest):
    return service.create_user(user)
