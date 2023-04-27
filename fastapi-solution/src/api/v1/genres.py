from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from models import Genres, _Genre  # noqa
from services import GenreService, get_genre_service

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
    '/<{genre_id}:UUID>/',
    response_model=GenreAPI,
    summary='Search genre',
    description='Search genre by id',
    response_description='Full genre details',
)
async def genre_details(
    genre_id: UUID, genre_service: GenreService = Depends(get_genre_service)
) -> GenreAPI | HTTPException:
    genre = await genre_service.get_by_id(genre_id)
    return GenreAPI(**genre.dict(by_alias=True))


@router.get(
    '',
    response_model=GenresAPI,
    summary='Genres',
    description='Genres with sorting',
    response_description='Summary of genres',
)
async def genres_main(
    sort: str | None = None,
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    genre_service: GenreService = Depends(get_genre_service),
) -> GenresAPI | HTTPException:
    genres = await genre_service.search(sort_by=sort, page=page, page_size=page_size)
    return GenresAPI(genres=genres)


@router.get(
    '/search',
    response_model=GenresAPI,
    summary='Search genres',
    description='Full-text search of genres with sorting',
    response_description='Summary of genres',
)
async def genres_details(
    query: str | None = None,
    sort: str | None = None,
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    genre_service: GenreService = Depends(get_genre_service),
) -> GenresAPI | HTTPException:
    genres = await genre_service.search(query, sort_by=sort, page=page, page_size=page_size)
    return GenresAPI(genres=genres)
