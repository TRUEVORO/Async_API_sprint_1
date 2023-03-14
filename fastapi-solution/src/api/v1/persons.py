from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models import Persons, _Person
from services.person import PersonService, get_person_service

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
    '/uuid',
    response_model=PersonAPI,
    summary='Search person',
    description='Search person by id',
    response_description='Full info of the specific person',
)
async def person_details(person_id: UUID, person_service: PersonService = Depends(get_person_service)) -> PersonAPI:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonAPI(uuid=person.uuid, full_name=person.full_name, movies=person.movies)


@router.get(
    '',
    response_model=PersonsAPI,
    summary='Popular persons',
    description='Popular persons sorted by rating',
    response_description='Short info of the persons sorted by full name',
)
async def persons_main(person_service: PersonService = Depends(get_person_service)) -> PersonsAPI:
    persons = await person_service.search()
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonsAPI(persons=persons)


@router.get(
    '/search',
    response_model=PersonsAPI,
    summary='Search persons',
    description='Full-text search of persons',
    response_description='Short info of the person with similar ones',
)
async def persons_details(query: str, person_service: PersonService = Depends(get_person_service)) -> PersonsAPI:
    persons = await person_service.search(query)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonsAPI(persons=persons)
