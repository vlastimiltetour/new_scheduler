import pytest 
from unittest.mock import MagicMock
from typing import List, Optional  # Importujeme potřebné typy
from dataclasses import dataclass
from datetime import datetime, timedelta, time
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


# Commands to run the test
# python3 -m pytest app/tests/unit/test_services.py
# python3 -m pytest app/tests/unit/test_services.py -vv

# Specific test
# python3 -m pytest app/tests/unit/test_services.py::test_get_persons -vv

from datetime import datetime, time
from unittest.mock import Mock
from uuid import uuid4



def test_get_person_availability():
    # Arrange
    
    person_id = uuid4()

    dao = Mock()

    dao

    service = AvailabilityService(
        dao=dao,
        start_frame=datetime(2026, 1, 1, 9, 0),   # Monday
        end_frame=datetime(2026, 1, 1, 12, 0),
    )


    # Act
    #result = service.get_unavailable_slots(person=person)
    result = service.get_slots_per_person(person_id)

    # Assert
    assert len(result) == 3
    assert type(result) == list
    


   