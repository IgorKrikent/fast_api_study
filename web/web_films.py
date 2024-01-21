from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from storage import storage

import constants

router = APIRouter(
    prefix='',
    tags=['WEB', 'Films']
)

templates = Jinja2Templates(directory='templates')

page_limit = 10


@router.get('/')
def main_page(request: Request, first_page: bool = True):

    context = {
        "request": request,
        "title": "Кинофонд",
        "movies": storage.get_content(page=first_page, page_limit=page_limit),
        "genres": constants.genres_list
    }

    return templates.TemplateResponse(name='main_page.html', context=context)


@router.get('/{page}')
def get_page(request: Request, page: int, search_result=None):

    context = {
        "request": request,
        "page": page,
        "movies": search_result,
        "genres": constants.genres_list,
    }

    return templates.TemplateResponse(name='search_page.html', context=context)


@router.post('/search')
@router.get("/search/{genre}")
def search_film(request: Request, search_param: str = Form(None), genre: str = None):

    if genre:

        detected_movies = storage.get_films_by_genre(genre=genre)
        title = f"{genre}"

    else:

        detected_movies = storage.get_film_by_name(skip=0, limit=page_limit, search_param=search_param)
        title = f"Результат поиска по запросу {search_param}"

    context = {
        "request": request,
        "title": title,
        "movies": detected_movies,
        "genres": constants.genres_list,
        # "search_by": genre if genre else search_param
    }

    return templates.TemplateResponse(name='search_page.html', context=context)


@router.get('/movie/{film_uuid}')
def get_one(request: Request, film_uuid: str, redirected: bool = False):

    saved_movie = storage.get_film(film_id=film_uuid)

    if saved_movie:

        context = {
            "request": request,
            "title": saved_movie['title'],
            "movie": saved_movie,
            "genres": constants.genres_list,
            "redirected": redirected
        }

        return templates.TemplateResponse(name='movie_page.html', context=context)

    context = {
        "request": request,
        "title": f'Фильм не найден',
        "genres": constants.genres_list
    }

    return templates.TemplateResponse(name='not_found.html', context=context)


@router.post('/rate/{film_uuid}')
def rate_film(request: Request, film_uuid: str, liked_it: str = Form(None)):

    storage.rate_film(film_id=film_uuid, like_it=int(liked_it))

    return get_one(request=request, film_uuid=film_uuid, redirected=True)
