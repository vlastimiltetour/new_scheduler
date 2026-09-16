#export PYTHONPATH=$PYTHONPATH:.
# make sure you have all packages running and installed from requirements
# python3 -m pytest
# python3 -m pytest ./app/tests/test_dao.py
# python3 -m pytest ./app/tests/test_services.py

import pytest 
import os
import shutil
from unittest.mock import MagicMock
from typing import List, Optional 
from dataclasses import dataclass
from datetime import datetime, timedelta, time
from app.services.persons import PersonService
from app.services.availability import AvailabilityService
from app.models.person import Person
from app.models.interviewer import Interviewer
from app.models.candidate import Candidate
from app.models.timeslot import TimeSlot
from app.models.workhours import WorkHours
from app.models.interview import Interview
from app.services.scheduler import InterviewScheduler
from app.dao.person_dao import PersonDao
from app.dao.interview_dao import InterviewDao
from app.dao.timeslot_dao import TimeSlotDao
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, clear_mappers
from app.dao.orm import start_mappers, metadata # ORM: Imperative mapping, metadata for tables
from datetime import datetime, time
from unittest.mock import MagicMock
from uuid import uuid4


# Elementary fixtures
@pytest.fixture()
def postgres_container():
    """Spins up a Docker container with Postgres."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture
def db_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    
    # Vytvoří tabulky v prázdném kontejneru podle tvých Python tříd
    metadata.create_all(bind=engine)
    
    yield engine
    engine.dispose()

# Test Scenario 
@dataclass
class TestScenario:
    person: Person
    person_service: PersonService
    availability_service: AvailabilityService
    blocked_slots: list[TimeSlot]

# Scenario Fixtures
@pytest.fixture
def sample_person_scenario(db_engine):
    person = Candidate(id=uuid4(), name="Sandra Mohawk", email="sandra_mohawk@greatestcandidate.com", person_type="candidate") 

    person_dao = PersonDao(db_engine)
    
    person_service = PersonService(dao=person_dao)
    person = person_service.create_person(person)

    #blocked_slots = []
    timeslot_dao = TimeSlotDao(db_engine)


    eu_workhours = WorkHours(1,start_time=time(9,00), end_time=time(16,00), workdays={0,1,2,3,4})

    availability_service = AvailabilityService(dao=timeslot_dao,start_frame=datetime(2026,4,6,9), end_frame=datetime(2026,4,6,17),workhours=eu_workhours)

    return TestScenario(
        person=person,
        person_service=person_service,
        availability_service=availability_service,
        blocked_slots=[]
    )

    