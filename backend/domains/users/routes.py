from fastapi import APIRouter

from .schemas import CreateUserRequest
from .service import UserService

router = APIRouter()
service = UserService()


@router.get("/users/", tags=["users"])
async def get_users():
    return service.get_users()


@router.get("/users/{name}", tags=["users"])
async def get_user(name: str):
    return service.get_user(name)


@router.post("/users/", tags=["users"])
async def create_user(user: CreateUserRequest):
    return service.create_user(user)
