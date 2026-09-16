import pytest 
from unittest.mock import MagicMock
from typing import List, Optional  # Importujeme potřebné typy



# Commands to run the test
# python3 -m pytest app/tests/integration/test_person_services.py
# python3 -m pytest app/tests/integration/test_person_services.py -vv

# Specific test
# python3 -m pytest app/tests/api/test_api.py::test_get_persons -vv

def test_postgres(postgres_container):
    print("CONTAINER:", postgres_container.get_connection_url())

def test_get_slots_per_person(sample_person_scenario):
    # Arrange 
    scenario = sample_person_scenario

    person_id = scenario.person.id
    person_service = scenario.person_service
    availability_service = scenario.availability_service
    blocked_slots = scenario.blocked_slots

    # Act
    retrieved_slots = availability_service.get_slots_per_person(
        person_id=person_id,
        slot_duration=60)
    
    #Assert
    assert len(retrieved_slots) == 8
