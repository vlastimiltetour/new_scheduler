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
from app.services.availability import Availability
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



@pytest.fixture
def sample_person():
    return Person(name="Sample_Person", email="person@person.com", person_type="person")

@pytest.fixture
def sample_candidate():
    return Candidate(name="Sample_Candidate", email="Candidate@Candidate.com", person_type="candidate")

@pytest.fixture
def sample_interviewer():
    return Interviewer(name="Sample_Interviewer", email="Interviewer@Interviewer.com", person_type="interviewer")

@pytest.fixture
def candidate_alan():
    return Candidate(name= "Alan Harper", email="alan@harper.com", person_type="candidate")

@pytest.fixture
def interviewer_johnny():
    return Interviewer(name="Johny Everpure", email="johny@everpure.com", person_type="interviewer")

@pytest.fixture
def interviewer_carl():
    return Interviewer(name="Carl_Uberinterviewer", email="carl@everpure.com", person_type="interviewer")

@pytest.fixture
def eu_workhours(): #last working hour slot is 16,00
    return WorkHours(1,start_time=time(9,00), end_time=time(16,00), workdays={0,1,2,3,4})

@pytest.fixture
def sample_availability_service(eu_workhours, db_engine):
    return Availability(now=datetime(2026,2,28,9,00), calendar_period=datetime(2027,1,1,9,00), workhours=eu_workhours, timeslotdao=TimeSlotDao(engine=db_engine))

@pytest.fixture
def sample_johnny_blocked_slots():
    return TimeSlot(start_time=datetime(2026,4,9,16,30), end_time=datetime(2026, 4, 9, 19,00), person=interviewer_johnny, owner_type="Candidate",status="unavailable")

@pytest.fixture
def sample_alan_blocked_slots():
    return TimeSlot(start_time=datetime(2026,3,2,11,30), end_time=datetime(2026, 3, 2, 15,00), person=candidate_alan, owner_type="Candidate",status="unavailable")

@pytest.fixture
def sample_carl_blocked_slots_1():
    return TimeSlot(start_time=datetime(2026,3,2,9,00), end_time=datetime(2026, 3, 2, 10,30), person=interviewer_carl, owner_type="Candidate",status="unavailable")

@pytest.fixture
def sample_carl_blocked_slots_2():
    return TimeSlot(start_time=datetime(2026,4,9,16,30), end_time=datetime(2026, 4, 9, 19,00), person=interviewer_carl, owner_type="Candidate",status="unavailable")

@pytest.fixture
def sample_end_scheduling_timeframe():
    return datetime(2026, 4, 10, 17, 00)

@pytest.fixture
def sample_scheduled_interview_carl_alan(candidate_alan, interviewer_carl):
    return Interview(candidate=candidate_alan, interviewer=interviewer_carl, timeslot=datetime(2026,3,2,11,00))