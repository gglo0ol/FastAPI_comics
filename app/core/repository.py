from core.db import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.model.base import Comic, Rating
from core.schemas import ComicCrete, ComicRead, RatingRead, RatingCreate
from sqlalchemy import select


class Repository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def comic_create(self, comic_data: ComicCrete) -> Comic:
        db_comic = Comic(title=comic_data.title, author=comic_data.author)
        self.db.add(db_comic)
        await self.db.commit()
        await self.db.refresh(db_comic)
        return await self.comic_read(db_comic.id)

    async def comic_update(self, comic_id: int, comic_update_data: ComicCrete) -> Comic:
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
        return "Comic not found"

    async def comic_delete(self, comic_id: int) -> dict | str:
        db_comic = (
            await self.db.execute(select(Comic).where(Comic.id == comic_id))
        ).scalar()
        if db_comic:
            await self.db.delete(db_comic)
            await self.db.commit()
            return {"status": "true", "message": "The menu has been deleted"}
        return "Comic not found"

    async def rating_create(self): ...

    async def rating_update(self): ...

    async def rating_read(self): ...

    async def rating_delete(self): ...
