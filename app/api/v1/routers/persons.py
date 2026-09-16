from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.persons import PersonCreate, PersonRead, PersonReplace, PersonPatch
from app.schemas.availability import PersonAvailabilitySlotResponse, AvailabilityQuery, AddPersonAvailabilitySlot
from app.dao.person_dao import PersonDao
from app.dao.timeslot_dao import TimeSlotDao
from app.services.persons import PersonService
from app.services.availability import AvailabilityService
from app.dao.database import engine
import datetime

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

'''
Router                         Service
──────────────────────────────────────────
post_person()       ────────→ create_person()

get_person()        ────────→ get_person()

get_persons()       ────────→ get_all_persons()

put_person()        ────────→ update_person()
                              
patch_person()      ────────→ update_person()

delete_person()     ────────→ delete_person()
'''

router = APIRouter()

def get_person_service() -> PersonService: #TODO rewrite this into a Session? 
    dao = PersonDao(engine())
    return PersonService(dao=dao)

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

@router.put("/{person_id}", response_model=PersonRead, status_code=status.HTTP_200_OK)
def update_person(
    person_id: str,
    data: PersonReplace,
    service: PersonService = Depends(get_person_service)) -> PersonRead:
    return service.update_person(person_id, data)

@router.patch("/{person_id}", response_model=PersonRead, status_code=status.HTTP_200_OK)
def update_person(
    person_id: str,
    data: PersonPatch,
    service: PersonService = Depends(get_person_service)) -> PersonRead:
    updated_data = data.model_dump(exclude_unset=True)
    return service.update_person(person_id, updated_data)

@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: str, 
    service: PersonService = Depends(get_person_service)) -> None:

    deleted = service.delete_person(person_id=person_id) # TODO delete depdendency on TIMESLOT

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person ID {person_id} wasn't found.")


# Availability Design
'''
GET    /persons/{personId}/availabilities
POST   /persons/{personId}/availabilities

GET    /persons/{personId}/availabilities/{availabilityId}
PUT    /persons/{personId}/availabilities/{availabilityId}
DELETE /persons/{personId}/availabilities/{availabilityId}
'''

def get_availability_service() -> AvailabilityService: 
    dao = TimeSlotDao(engine())
    return AvailabilityService(dao=dao)

@router.post("/{person_id}/availabilites", status_code=status.HTTP_201_CREATED)
def add_person_availability(person_id: str,
                            query: AddPersonAvailabilitySlot = Depends(),
                            service: AvailabilityService = Depends(get_availability_service),
                           ) -> PersonAvailabilitySlotResponse:

    return service.add_person_availability(person_id, query=query)

@router.get("/{person_id}/availabilities", response_model=list[PersonAvailabilitySlotResponse], status_code=status.HTTP_200_OK)
def get_person_availability(person_id: str, 
                            query: AvailabilityQuery = Depends(),
                            service: AvailabilityService = Depends(get_availability_service)
                            ) -> list[PersonAvailabilitySlotResponse]:

    person_availability = service.get_slots_per_person(person_id, query=query)
    
    if not person_availability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Osoba s ID {person_id} nebyla nalezena.")

    return person_availability
