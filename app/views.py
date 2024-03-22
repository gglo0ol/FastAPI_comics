from fastapi import APIRouter, Depends
from core.schemas import ComicRead, RatingCreate, RatingRead, ComicCrete
from core.repository import Repository


router_comic = APIRouter(tags=["Comics"], prefix="/api/comics")
router_rating = APIRouter(tags=["Rating"], prefix="/api/ratings")


@router_comic.post(path="/", response_model=ComicRead, status_code=201)
async def create_comics(
    comic_data: ComicCrete, repo: Repository = Depends()
) -> ComicRead:
    return await repo.comic_create(comic_data=comic_data)


@router_comic.get(path="/{comic_id}/", response_model=ComicRead)
async def get_comics(comic_id: int, repo: Repository = Depends()) -> ComicRead | str:
    return await repo.comic_read(comic_id=comic_id)


@router_comic.patch(path="/{comic_id}/", response_model=ComicRead)
async def update_comics(
    comic_id: int, data: ComicCrete, repo: Repository = Depends()
) -> ComicRead:
    return await repo.comic_update(comic_id=comic_id, comic_update_data=data)


@router_comic.delete(path="/{comic_id}/")
async def delete_comics(comic_id: int, repo: Repository = Depends()) -> dict | str:
    return await repo.comic_delete(comic_id=comic_id)


@router_rating.post(path="/")
async def create_rating(rating_create_data: RatingCreate):
    return rating_create_data


@router_rating.get(path="/{comic_id}/rating/")
async def get_rating(comic_id: str):
    return comic_id
