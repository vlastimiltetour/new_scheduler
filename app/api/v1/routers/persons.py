from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.persons import PersonCreate, PersonRead
from app.dao.person_dao import PersonDao
from app.models.person import Person
from app.services.persons import PersonService
from app.dao.database import engine

# Router handles HTTP. Service handles business logic. DAO handles persistence.


'''
HTTP method	API endpoint	Description
GET	/customers	Get a list of customers.
GET	/customers/<customer_id>	Get a single customer.
POST	/customers	Create a new customer.
PUT	/customers/<customer_id>	Update a customer.
PATCH	/customers/<customer_id>	Partially update a customer.
DELETE	/customers/<customer_id>	Delete a customer.
'''

router = APIRouter()

def get_person_service() -> PersonService: #TODO rewrite this into a Session? 
    dao = PersonDao(engine())
    return PersonService(p_dao=dao)

@router.get("/", response_model=list[PersonRead], status_code=status.HTTP_200_OK,)
def get_all_persons(
    service: PersonService = Depends(get_person_service)) -> list[PersonRead]:
    return service.get_all_persons()

@router.get("/{person_id}", response_model=PersonRead, status_code=status.HTTP_200_OK)
def get_person(person_id: str, service: PersonService = Depends(get_person_service)) -> PersonRead:
    person = service.read_person(person_id)
    
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Osoba s ID {person_id} nebyla nalezena.")
    return person


@router.post("/", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
def create_person(
    data: PersonCreate,
    service: PersonService = Depends(get_person_service)) -> PersonRead:
    return service.create_person(data)

# TODO update
'''@router.post("/", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
def create_person(
    data: PersonCreate,
    service: PersonService = Depends(get_person_service)) -> PersonRead:
    new_person = Person(name=data.name, email=data.email, person_type=data.person_type)

    return service.create_person(data)'''

@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: str, 
    service: PersonService = Depends(get_person_service)) -> None:

    deleted = service.delete_person(person_id=person_id) # TODO delete depdendency on TIMESLOT

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person ID {person_id} wasn't found.")