from pydantic import BaseModel, Field
from datetime import datetime
import constants


class CreatedBy(BaseModel):

    director: list[str] = Field(examples=[['Frank Miller', 'Quentin Tarantino']], default=[])
    producer: list[str] = Field(examples=[['Jason Bloom', 'George Lucas']], default=[])
    scriptwriter: list[str] = Field(examples=[['M. Night Shyamalan', 'Christopher Nolan']], default=[])


class AnnouncedFilm(BaseModel):

    title: str = Field(examples=['Some Movie'])
    genres: list[constants.Genres] = Field(default=[])
    description: str = None


class FilmData(AnnouncedFilm):

    created_by: CreatedBy
    cast: list[str]
    duration: int = Field(gt=0)
    tags: list = Field(default=[], max_items=5)
    rating: float = 0.0
    votes: int = 0
    poster: str = ''
    year: int = Field(gt=1895, lt=datetime.today().year, default=None)


class SavedFilm(FilmData):

    uuid: str = Field(examples=['dedf37e7-70c4-40f6-901d-5bc6be9631ce'])
