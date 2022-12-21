from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models import Genres, _Genre
from services.genre import GenreService, get_genre_service

router = APIRouter(
    prefix='/api/v1/genres',
    tags=['genres'],
)


class GenreAPI(_Genre):
    """API model for genre."""

    pass


class GenresAPI(Genres):
    """API model for list of genres."""

    pass


@router.get(
    '/uuid',
    response_model=GenreAPI,
    summary='Search genre',
    description='Search genre by id',
    response_description='Full info of the specific genre',
)
async def genre_details(genre_id: UUID, genre_service: GenreService = Depends(get_genre_service)) -> GenreAPI:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return GenreAPI(uuid=genre.uuid, name=genre.name)


@router.get(
    '',
    response_model=GenresAPI,
    summary='Genres',
    description='Genres',
    response_description='Genres sorted by names',
)
async def genres_main(genre_service: GenreService = Depends(get_genre_service)) -> GenresAPI:
    genres = await genre_service.search()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return GenresAPI(genres=genres)


@router.get(
    '/search',
    response_model=GenresAPI,
    summary='Search genres',
    description='Full-text search of genres',
    response_description='Short info of the genre with similar ones',
)
async def genres_details(query: str, genre_service: GenreService = Depends(get_genre_service)) -> GenresAPI:
    genres = await genre_service.search(query)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return GenresAPI(genres=genres)
