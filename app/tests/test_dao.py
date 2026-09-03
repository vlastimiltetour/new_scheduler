import pytest 
from unittest.mock import MagicMock
from typing import List, Optional  # Importujeme potřebné typy
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

from app.tests.conftest import interviewer_johnny, sample_johnny_blocked_slots, db_engine

def test_save_and_get_interview(db_engine, candidate_alan, interviewer_carl, sample_scheduled_interview_carl_alan):
    person_db = PersonDao(engine=db_engine)
    person_db.save(candidate_alan)
    person_db.save(interviewer_carl)

    interview_db = InterviewDao(engine=db_engine)
    interview_db.save(sample_scheduled_interview_carl_alan)

    retrieved_interview = interview_db.get_object_by_id(sample_scheduled_interview_carl_alan.id)
    assert retrieved_interview.timeslot == datetime(2026,3,2,11,00)
    

def test_save_and_get_person(db_engine, sample_person):
    person_db = PersonDao(engine=db_engine)
    print('initiating db save')
    person_db.save(sample_person)
    print('post db save')

    retrieved_person = person_db.get_object_by_id(sample_person.id)

    assert retrieved_person.name == "Sample_Person"
    assert retrieved_person.email == "person@person.com"
    assert retrieved_person.person_type == "person"

def test_and_save_multiple_persons(db_engine, sample_person, candidate_alan, interviewer_johnny, interviewer_carl):
    person_db = PersonDao(engine=db_engine)
    person_db.save(sample_person)
    person_db.save(candidate_alan)
    person_db.save(interviewer_johnny)
    person_db.save(interviewer_carl)

    retrieved_sample_person = person_db.get_object_by_id(sample_person.id)
    retrieved_candidate_alan = person_db.get_object_by_id(candidate_alan.id)
    retrieved_interviewer_johnny = person_db.get_object_by_id(interviewer_johnny.id)
    retrieved_interviewer_carl = person_db.get_object_by_id(interviewer_carl.id)

    assert retrieved_sample_person.name == "Sample_Person"
    assert retrieved_candidate_alan.name == "Alan Harper"
    assert retrieved_interviewer_johnny.name == "Johny Everpure"
    assert retrieved_interviewer_carl.name == "Carl_Uberinterviewer"

def test_delete_person(db_engine, sample_person):
    person_db = PersonDao(engine=db_engine)
    person_db.save(sample_person)
    person_db.delete(sample_person.id)
    # testing retrieval and changing name of the variable to avoid in memory object in RAM
    retrieved_after_delete = person_db.get_object_by_id(sample_person.id) 
    assert retrieved_after_delete is None

def test_update_person(db_engine, sample_person):
    person_db = PersonDao(engine=db_engine)
    print('initiating db save')
    person_db.save(sample_person)
    print('post db save')

    person_db.update(Person(id=1, name="Carlos", email="carlos@carlos.io"))
    # testing retrieval and changing name of the variable to avoid in memory object in RAM
    updated_person = person_db.get_object_by_id(sample_person.id) 
    assert updated_person.name == "Carlos"
    assert updated_person.email == "carlos@carlos.io"

def test_save_and_get_slot(db_engine,sample_johnny_blocked_slots, interviewer_johnny, sample_alan_blocked_slots, candidate_alan, interviewer_carl, sample_carl_blocked_slots_1, sample_carl_blocked_slots_2):
    slot_db = TimeSlotDao(engine=db_engine)
    person_db = PersonDao(engine=db_engine)
    
    person_db.save(interviewer_johnny)
    person_db.save(candidate_alan)
    person_db.save(interviewer_carl)

    slot_db.save(sample_johnny_blocked_slots)
    slot_db.save(sample_alan_blocked_slots)
    slot_db.save(sample_carl_blocked_slots_1)
    slot_db.save(sample_carl_blocked_slots_2)


    assert sample_johnny_blocked_slots.owner_type == "Interviewer"
    #assert len(slot_db.get_blocked_slots_by_person(interviewer_johnny.id)) == 0

    assert sample_alan_blocked_slots.owner_type == "Candidate"
    #assert len(slot_db.get_blocked_slots_by_person(candidate_alan.id)) == 0


def test_blocked_slot():
    pass 

def test_alan_blocker_slots(sample_alan_blocked_slots, candidate_alan):
    pass
