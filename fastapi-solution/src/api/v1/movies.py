from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models import MovieFull, Movies
from services.movie import MovieService, get_movie_service

router = APIRouter(
    prefix='/api/v1/movies',
    tags=['movies'],
)


class MoviesAPI(Movies):
    """API model for list of movies."""

    pass


class MovieAPIFull(MovieFull):
    """API model for movie with full description."""

    pass


@router.get(
    '/{movie_id}',
    response_model=MovieAPIFull,
    summary='Search movie',
    description='Search movie by id',
    response_description='Full info of the specific movie',
)
async def movie_details(movie_id: UUID, movie_service: MovieService = Depends(get_movie_service)) -> MovieAPIFull:
    movie = await movie_service.get_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='movie not found')
    return MovieAPIFull(uuid=movie.uuid, title=movie.title, imdb_rating=movie.imdb_rating)


@router.get(
    '',
    response_model=MoviesAPI,
    summary='Popular movies',
    description='Popular movies sorted by rating',
    response_description='Short info of the movies sorted by rating',
)
async def movies_main(movie_service: MovieService = Depends(get_movie_service)) -> MoviesAPI:
    movies = await movie_service.search()
    if not movies:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='movie not found')
    return MoviesAPI(movies=movies)


@router.get(
    '/search/{text}',
    response_model=MoviesAPI,
    summary='Search movies',
    description='Full-text search of movies',
    response_description='Short info of the movie with similar ones',
)
async def movies_details(query: str, movie_service: MovieService = Depends(get_movie_service)) -> MoviesAPI:
    movies = await movie_service.search(query)
    if not movies:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='movie not found')
    return MoviesAPI(movies=movies)
