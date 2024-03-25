from sqlalchemy.exc import NoResultFound

from core.db import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.model.base import Comic, Rating
from core.schemas import ComicCreate, ComicRead, RatingRead, RatingCreate
from sqlalchemy import select, func


class Repository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def comic_create(self, comic_data: ComicCreate) -> Comic:
        db_comic = Comic(title=comic_data.title, author=comic_data.author)
        self.db.add(db_comic)
        await self.db.commit()
        await self.db.refresh(db_comic)
        return await self.comic_read(db_comic.id)

    async def comic_update(
        self, comic_id: int, comic_update_data: ComicCreate
    ) -> Comic:
        db_comic = (
            await self.db.execute(select(Comic).where(Comic.id == comic_id))
        ).scalar()
        if db_comic:
            db_comic.title, db_comic.author = (
                comic_update_data.title,
                comic_update_data.author,
            )
            await self.db.commit()
            await self.db.refresh(db_comic)
            return await self.comic_read(db_comic.id)

    async def comic_read(self, comic_id: int) -> Comic | str:
        comic = (
            await self.db.execute(select(Comic).where(Comic.id == comic_id))
        ).scalar()
        if comic:
            return comic
        raise NoResultFound("Comic not found")

    async def comic_update_rating(self, comic_id: int) -> None:
        db_comic = await self.comic_read(comic_id=comic_id)
        rating = await self.get_avg_rating(comic_id=comic_id)
        db_comic.rating = rating
        await self.db.commit()
        await self.db.refresh(db_comic)

    async def comic_delete(self, comic_id: int) -> dict | str:
        db_comic = (
            await self.db.execute(select(Comic).where(Comic.id == comic_id))
        ).scalar()
        if db_comic:
            await self.db.delete(db_comic)
            await self.db.commit()
            return {"status": "true", "message": "The menu has been deleted"}
        return "Comic not found"

    async def rating_create(self, rating_create_data: RatingCreate) -> str:
        comic_id = rating_create_data.comic_id
        db_comic = await self.comic_read(comic_id=comic_id)
        if db_comic:
            db_rating = (
                await self.db.execute(
                    select(Rating).where(
                        Rating.comic_id == comic_id,
                        Rating.user_id == rating_create_data.user_id,
                    )
                )
            ).scalar()
            if db_rating:
                db_rating.value = rating_create_data.value
            else:
                db_rating = Rating(
                    comic_id=comic_id,
                    user_id=rating_create_data.user_id,
                    value=rating_create_data.value,
                )
                self.db.add(db_rating)
            rating_id = db_rating.id
            await self.db.commit()
            await self.db.refresh(db_rating)
            await self.comic_update_rating(comic_id=comic_id)
            return "Success, rating create"

    async def rating_update(self): ...

    async def rating_read(self, rating_id: int) -> Rating:
        db_rating = (
            await self.db.execute(select(Rating).where(Rating.id == rating_id))
        ).scalar()
        if db_rating:
            return db_rating
        raise NoResultFound("Rating not found")

    async def get_avg_rating(self, comic_id: int) -> int:
        avg = (
            await self.db.execute(
                select(func.avg(Rating.value)).where(Rating.comic_id == comic_id)
            )
        ).scalar()
        return avg

    async def rating_delete(self): ...
