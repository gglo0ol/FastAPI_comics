from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound

from core.schemas import ComicRead, RatingCreate, RatingRead, ComicCreate
from core.repository import Repository


router_comic = APIRouter(tags=["Comics"], prefix="/api/comics")
router_rating = APIRouter(tags=["Rating"], prefix="/api/ratings")


@router_comic.post(path="/", response_model=ComicRead, status_code=201)
async def create_comics(
    comic_data: ComicCreate, repo: Repository = Depends()
) -> ComicRead:
    return await repo.comic_create(comic_data=comic_data)


@router_comic.get(
    path="/{comic_id}/",
    response_model=ComicRead,
    summary="Вывести данные коммикса",
    responses={404: {"description": "Comic not found"}},
)
async def get_comics(comic_id: int, repo: Repository = Depends()) -> ComicRead | str:
    try:
        return await repo.comic_read(comic_id=comic_id)
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router_comic.patch(path="/{comic_id}/", response_model=ComicRead)
async def update_comics(
    comic_id: int, data: ComicCreate, repo: Repository = Depends()
) -> ComicRead:
    return await repo.comic_update(comic_id=comic_id, comic_update_data=data)


@router_comic.delete(path="/{comic_id}/")
async def delete_comics(comic_id: int, repo: Repository = Depends()) -> dict | str:
    return await repo.comic_delete(comic_id=comic_id)


@router_rating.post(path="/", status_code=201)
async def create_rating(
    rating_create_data: RatingCreate, repo: Repository = Depends()
) -> RatingRead | str:
    try:
        return await repo.rating_create(rating_create_data=rating_create_data)
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


# @router_rating.get(path="/{comic_id}/rating/")
# async def get_rating(comic_id: int, repo: Repository = Depends()) -> list[ComicRead]:
#     try:
#         return await repo.rating_read(comic_id=comic_id)
#     except NoResultFound as error:
#         raise HTTPException(status_code=404, detail=error.args[0])


@router_rating.get(
    path="/{comic_id}/rating/",
    summary="Возвращает средний рейтинг коммикса",
    response_model=float,
)
async def get_avg_rating(comic_id: int, repo: Repository = Depends()) -> float:
    return await repo.get_avg_rating(comic_id=comic_id)
