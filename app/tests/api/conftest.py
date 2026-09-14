from fastapi.testclient import TestClient
from app.api.v1.routers.persons import get_person_service
import pytest 
from main import app

# Fast and Clean, no calls to DB

# you're creating an object that behaves somewhat like an HTTP client/browser, but instead of making requests over the network to something like:
# This would run as integration test - calling a db
'''@pytest.fixture
def client():
    return TestClient(app) '''

# This is a mock to the Service, no calls to DB
@pytest.fixture
def client(person):
    class FakeService:
        def get_all_persons(self):
            return [person]

        def read_person(self, person_id):
            return person if person_id == person["id"] else None

        def create_person(self, data):
            return person
        
        def update_person(self, person_id, data):
            if hasattr(data, "model_dump"): 
                # Pydantic v2 model: dump only explicitly provided fields
                data_dict = data.model_dump(exclude_unset=True)
     
            elif isinstance(data, dict): 
                # Raw Python dictionary 
                data_dict = data
                
         

            return {**person, **data_dict}

        def delete_person(self, person_id):
            return True

    app.dependency_overrides[get_person_service] = FakeService

    yield TestClient(app)

    app.dependency_overrides.clear()



# Prep Fixture -> Full Pydantic object Person
@pytest.fixture
def person():
    return {
        "id": "58aa5567-1f99-41ae-8499-50a0c4be152b",
        "name": "Jan Novak",
        "email": "jan@example.com",
        "person_type": "interviewer",
    }

@pytest.fixture
def payload(person):
    return {
        k: v for k, v in person.items()
        if k!= "id"
    }