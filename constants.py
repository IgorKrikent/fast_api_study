from enum import Enum


class Genres(str, Enum):

    FICTION = 'Фантастика'
    DRAMA = 'Драма'
    FANTASY = 'Фэнтези'
    THRILLER = 'Триллер'
    ACTION_MOVIE = 'Боевик'
    COMEDY = 'Комедия'
    HORROR = 'Ужасы'
    MELODRAMA = 'Мелодрама'
    DETECTIVE = 'Детектив'
    WESTERN = 'Вестерн'
    CRIME = 'Криминал'


genres_list = []

for genre in Genres:

    genres_list.append(genre.value)
