from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from models import MovieFull, Movies
from services import MovieService, get_movie_service

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
    '/<{movie_id}:UUID>/',
    response_model=MovieAPIFull,
    summary='Search movie',
    description='Search movie by id',
    response_description='Full film details',
)
async def get_movie(
    movie_id: UUID, movie_service: MovieService = Depends(get_movie_service)
) -> MovieAPIFull | HTTPException:
    movie = await movie_service.get_by_id(uuid=movie_id)
    return MovieAPIFull(**movie.dict(by_alias=True))


@router.get(
    '',
    response_model=MoviesAPI,
    summary='Popular movies',
    description='Popular movies with sorting and filtering by genre',
    response_description='Summary of movies',
)
async def movies_main_page(
    sort: str | None = None,
    genre: str | None = None,
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    movie_service: MovieService = Depends(get_movie_service),
) -> MoviesAPI | HTTPException:
    movies = await movie_service.search(
        sort_by=sort, filter_by=('genres', genre) if genre else None, page=page, page_size=page_size
    )
    return MoviesAPI(movies=movies)


@router.get(
    '/search',
    response_model=MoviesAPI,
    summary='Search movies',
    description='Full-text search of movies with sorting and filtering by genre',
    response_description='Summary of movies',
)
async def search_movies(
    query: str | None = None,
    sort: str | None = None,
    genre: str | None = None,
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    movie_service: MovieService = Depends(get_movie_service),
) -> MoviesAPI | HTTPException:
    movies = await movie_service.search(
        query=query, sort_by=sort, filter_by=('genre', genre) if genre else None, page=page, page_size=page_size
    )
    return MoviesAPI(movies=movies)
