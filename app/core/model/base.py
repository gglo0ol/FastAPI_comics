from sqlalchemy.orm import relationship

from core.db import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Float


class Comic(Base):
    __tablename__ = "comics"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    rating = Column(Float, default=0)
    ratings = relationship(
        "Rating", back_populates="comic", cascade="all, delete-orphan"
    )


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    comic_id = Column(ForeignKey("comics.id"))
    user_id = Column(Integer)
    value = Column(Integer)
    comic = relationship("Comic", back_populates="ratings")
