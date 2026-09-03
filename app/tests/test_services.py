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


def test_get_slots_per_person_1_week_johnny(db_engine, sample_availability_service, sample_johnny_blocked_slots, interviewer_johnny, sample_end_scheduling_timeframe):
    # Arrange 
    person_db = PersonDao(engine=db_engine)
    person_db.save(interviewer_johnny)

    slots_db = TimeSlotDao(engine=db_engine)
    slots_db.save(sample_johnny_blocked_slots)

    # Act
    retrieved_slots = sample_availability_service.get_slots_per_person(
        interviewer_johnny,slot_duration=60, timeframe=sample_end_scheduling_timeframe)
    
    #Assert
    assert len(retrieved_slots) == 36

def test_get_slots_per_person_2_weeks(sample_availability_service, interviewer_johnny):
    
    retrived_slots = sample_availability_service.get_slots_per_person(
        interviewer_johnny,slot_duration=60, timeframe=datetime(2026, 3, 15, 11, 00))
    
    assert len(retrived_slots) == 76

def test_get_slots_alan(sample_availability_service, candidate_alan):
    retrived_slots = sample_availability_service.get_slots_per_person(
        candidate_alan,slot_duration=60, timeframe=datetime(2026, 3, 15, 11, 00))
    
    assert len(retrived_slots) == 77

def test_get_slots_carl(sample_availability_service, interviewer_carl):
    retrived_slots = sample_availability_service.get_slots_per_person(
        interviewer_carl,slot_duration=60, timeframe=datetime(2026, 3, 15, 11, 00))
    
    assert len(retrived_slots) == 78

def test_interview_scheduling_service_alan_johny(sample_availability_service,candidate_alan, interviewer_johnny, sample_interview_johny_alan):
    scheduler = InterviewScheduler()
    result = scheduler.schedule(sample_availability_service, candidate=candidate_alan, interviewers=[interviewer_johnny], interview_duration=60, timeframe=datetime(2026, 3, 15, 11, 00))

    assert result.id == sample_interview_johny_alan.id
    assert result.timeslot == sample_interview_johny_alan.timeslot



def test_interview_scheduling_service_alan_carl(sample_availability_service,candidate_alan, interviewer_carl, sample_interview_carl_alan):
    scheduler = InterviewScheduler()
    result = scheduler.schedule(sample_availability_service, candidate=candidate_alan, interviewers=[interviewer_carl], interview_duration=60, timeframe=datetime(2026, 3, 15, 11, 00))

    assert result.id == sample_interview_carl_alan.id
    assert result.timeslot == sample_interview_carl_alan.timeslot