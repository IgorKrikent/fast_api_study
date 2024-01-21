from fastapi import APIRouter, status
from storage import storage

import schemas

router = APIRouter(
    prefix='/api/films',
    tags=['API', 'Films']
)


@router.post('/post/', status_code=status.HTTP_201_CREATED)
def post_film(film: schemas.FilmData) -> schemas.SavedFilm:

    saved_film = storage.create_film(film.model_dump())

    return saved_film


@router.get('/')
def get_film_by_name(skip: int = 0, limit: int = 10, search_param: str = None) -> list[schemas.SavedFilm]:

    films = storage.get_film_by_name(skip=skip, limit=limit, search_param=search_param)

    return films


@router.put('/rate/{film_id}')
def rate_film(film_id: str, liked_it: bool):

    storage.rate_film(film_id=film_id, like_it=liked_it)

    return {"rated": "OK"}


@router.delete('/delete/{film_id}')
def delete_film(film_id: str):

    storage.delete_film(film_id=film_id)

    return {"deleted": True}
