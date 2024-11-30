from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from .schemas import Score, CreateScoreRequest
from .service import ScoreService

router = APIRouter()

score_service = ScoreService()


@router.get("/scores", response_model=List[Score])
async def get_scores(
        user_id: Optional[int] = Query(None),
        activity_id: Optional[int] = Query(None)):
    return score_service.get_scores(user_id, activity_id)




@router.post("/scores", response_model=Score)
async def create_score(
        score: CreateScoreRequest):
    try:
        return score_service.create_score(score)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/scores/{score_id}", response_model=Score)
async def update_score(score_id: int, score: Score):
    try:
        return score_service.update_score(score_id, score)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/scores/{score_id}", response_model=None)
async def delete_score(score_id: int):
    try:
        score_service.delete_score(score_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
