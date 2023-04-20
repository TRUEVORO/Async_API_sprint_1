from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models import Persons, _Person  # noqa
from services import PersonService, get_person_service

router = APIRouter(
    prefix='/api/v1/persons',
    tags=['persons'],
)


class PersonAPI(_Person):
    """API model for person."""

    pass


class PersonsAPI(Persons):
    """API model for list of persons."""

    pass


@router.get(
    '/<{person_id}:UUID>/',
    response_model=PersonAPI,
    summary='Search person',
    description='Search person by id',
    response_description='Full person details',
)
async def person_details(person_id: UUID, person_service: PersonService = Depends(get_person_service)) -> PersonAPI:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonAPI(uuid=person.uuid, full_name=person.full_name, films=person.films)


@router.get(
    '',
    response_model=PersonsAPI,
    summary='Popular persons',
    description='Popular genres with sorting',
    response_description='Summary of persons',
)
async def persons_main(
    sort: str | None = None,
    page: int = 1,
    page_size: int = 50,
    person_service: PersonService = Depends(get_person_service),
) -> PersonsAPI:
    persons = await person_service.search(sort_by=sort, page=page, page_size=page_size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')
    return PersonsAPI(persons=persons)


@router.get(
    '/search',
    response_model=PersonsAPI,
    summary='Search persons',
    description='Full-text search of persons',
    response_description='Short info of the person with similar ones',
)
async def persons_details(
    query: str | None = None,
    sort: str | None = None,
    page: int = 1,
    page_size: int = 50,
    person_service: PersonService = Depends(get_person_service),
) -> PersonsAPI:
    persons = await person_service.search(query=query, sort_by=sort, page=page, page_size=page_size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonsAPI(persons=persons)
