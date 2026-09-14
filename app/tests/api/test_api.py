import pytest 

# Commands to run the test
# python3 -m pytest app/tests/api/test_api.py
# python3 -m pytest app/tests/api/test_api.py -vv

# Specific test
# python3 -m pytest app/tests/api/test_api.py::test_get_persons -vv


def test_get_persons(client):
    response = client.get("/api/v1/persons/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_person(client, person):
    response = client.get(f"/api/v1/persons/{person['id']}")

    assert response.status_code == 200
    assert response.json() == person


def test_create_user(client, payload):
    response = client.post("/api/v1/persons/", json=payload)

    assert response.status_code == 201
    assert response.json()["name"] == "Jan Novak"

def test_put_user(client):
    
    updated_person = {
        "id": "58aa5567-1f99-41ae-8499-50a0c4be152b",
        "name": "Jared Howard",
        "email": "jared@howard.com",
        "person_type": "candidate",
    }

    response = client.put(f"/api/v1/persons/{updated_person['id']}", json=updated_person)
    
    assert response.status_code == 200

    data = response.json()
    assert data['name'] == "Jared Howard"
    
def test_patch_user(client):
    updated_person = {
            "id": "58aa5567-1f99-41ae-8499-50a0c4be152b",
            "name": "John Blow",
        }
    
    response = client.patch(f"/api/v1/persons/{updated_person['id']}", json=updated_person)
        
    assert response.status_code == 200

    data = response.json()
    assert data['name'] == "John Blow"
    
def test_delete_user(client, person):
    response = client.delete(f"/api/v1/persons/{person['id']}")

    assert response.status_code == 204
