from fastapi import APIRouter, Depends
from core.schemas import ComicRead, RatingCreate, RatingRead, ComicCrete
from core.repository import Repository


router = APIRouter(tags=["Comics"])


@router.post(path="/api/comics/")
async def create_comics(
    comic_data: ComicCrete, repo: Repository = Depends()
) -> ComicRead:
    return await repo.comic_create(comic_data=comic_data)


@router.post(path="/api/ratings/")
async def create_rating(rating_create_data: RatingCreate):
    return rating_create_data


@router.get(path="/api/comics/{comic_id}/rating/")
async def get_rating(comic_id: str):
    return comic_id
