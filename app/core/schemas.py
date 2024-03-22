from pydantic import BaseModel, Field


class ComicCrete(BaseModel):
    title: str
    author: str


class ComicRead(ComicCrete):
    id: int
    rating: float = Field(ge=0, le=5)


class RatingCreate(BaseModel):
    comic_id: int
    user_id: int
    value: int = Field(ge=1, le=5)


class RatingRead(RatingCreate):
    id: int
