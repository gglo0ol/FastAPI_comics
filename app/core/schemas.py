from pydantic import BaseModel, Field, field_validator


class ComicCreate(BaseModel):
    title: str
    author: str


class ComicRead(ComicCreate):
    id: int
    rating: float = Field(
        ge=0,
        le=5,
    )

    @field_validator("rating")
    @classmethod
    def result_check(cls, v: float):
        return round(v, 1)


class RatingCreate(BaseModel):
    comic_id: int
    user_id: int
    value: int = Field(ge=1, le=5)


class RatingRead(RatingCreate):
    id: int
