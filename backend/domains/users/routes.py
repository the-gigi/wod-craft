from http.client import HTTPException

from fastapi import APIRouter, HTTPException

from .schemas import CreateUserRequest
from .service import UserService

router = APIRouter()
service = UserService()


@router.get("/users/", tags=["users"])
async def get_users():
    return service.get_users()


@router.get("/users/{name}", tags=["users"])
async def get_user(name: str):
    try:
        return service.get_user(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/users/", tags=["users"])
async def create_user(user: CreateUserRequest):
    return service.create_user(user)
