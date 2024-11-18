from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import Activity, CreateActivityRequest
from .service import ActivityService

router = APIRouter()

activity_service = ActivityService()


@router.get("/activities", response_model=List[Activity])
async def get_activities():
    return activity_service.get_activities()


@router.get("/activities/{activity_id}", response_model=Activity)
async def get_activity(activity_id: int):
    activity = activity_service.get_activity(activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/activities", response_model=Activity)
async def create_activity(activity: CreateActivityRequest):
    try:
        return activity_service.create_activity(activity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/activities/{activity_id}", response_model=Activity)
async def update_activity(activity_id: int, activity: Activity):
    try:
        return activity_service.update_activity(activity_id, activity)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/activities/{activity_id}", response_model=None)
async def delete_activity(activity_id: int):
    try:
        activity_service.delete_activity(activity_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
