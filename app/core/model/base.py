from app.core.db import Base

from sqlalchemy import Column, Integer, String, ForeignKey


class Comic(Base):
    __tablename__ = "comics"
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String)
    author = Column(String)
    rating = Column(Integer, default=0)


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, unique=True)
    comic_id = Column(ForeignKey("comics.id"))
    user_id = Column(Integer)
    value = Column(Integer)  # Ограничение от 1 до 5, целые числа

    # Создайте модель Comic с полями:
    #
    # id (уникальный идентификатор)
    # title (название комикса)
    # author (автор комикса)
    # rating (рейтинг комикса, по умолчанию 0)
    # Создайте модель Rating с полями:
    #
    # id (уникальный идентификатор)
    # comic_id (ссылка на комикс)
    # user_id (идентификатор пользователя, оценившего комикс)
    # VALUE (оценка пользователя от 1 до 5)
