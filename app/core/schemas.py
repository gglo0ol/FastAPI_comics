from pydantic import BaseModel, Field


class Comic(BaseModel):
    id: int
    title: str
    author: str
    rating: float = Field(ge=1, le=5)


class Rating(BaseModel):
    id: int
    comic_id: int
    user_id: int
    value: int = Field(ge=1, le=5)
