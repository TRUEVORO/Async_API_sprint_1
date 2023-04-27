from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

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
async def person_details(
    person_id: UUID, person_service: PersonService = Depends(get_person_service)
) -> PersonAPI | HTTPException:
    person = await person_service.get_by_id(person_id)
    return PersonAPI(**person.dict(by_alias=True))


@router.get(
    '',
    response_model=PersonsAPI,
    summary='Popular persons',
    description='Popular genres with sorting',
    response_description='Summary of persons',
)
async def persons_main(
    sort: str | None = None,
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    person_service: PersonService = Depends(get_person_service),
) -> PersonsAPI | HTTPException:
    persons = await person_service.search(sort_by=sort, page=page, page_size=page_size)
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
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    person_service: PersonService = Depends(get_person_service),
) -> PersonsAPI | HTTPException:
    persons = await person_service.search(query=query, sort_by=sort, page=page, page_size=page_size)
    return PersonsAPI(persons=persons)
