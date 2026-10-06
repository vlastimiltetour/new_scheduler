from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import Optional, TYPE_CHECKING
from app.models.person import Person
from app.models.interviewer import Interviewer
from app.models.candidate import Candidate
from app.models.timeslot import TimeSlot
from app.models.workhours import WorkHours
from app.models.interview import Interview
from app.dao.person_dao import PersonDao
from app.dao.interview_dao import InterviewDao
from app.dao.timeslot_dao import TimeSlotDao
from app.schemas.availability import AvailabilityQuery, PersonAvailabilitySlotResponse, AddPersonAvailabilitySlot


class AvailabilityService:
    def __init__(self, dao: TimeSlotDao):
        # get slots from a calendar
        self.dao = dao # DAO dependency injection 
        # get holidays TODO

    def truncate_to_whole_hours(self):
        self.now = self.start_frame.replace(minute=0, second=0, microsecond=0)
        return self.now

    def is_within_workhours(self, slot):

        eu_workhours = WorkHours(
            id=1, 
            start_time=time(9, 0), 
            end_time=time(16, 0), 
            workdays={0, 1, 2, 3, 4}
        )
        
        if slot.weekday() not in eu_workhours.workdays:
            return False 
        
        if slot.time() < eu_workhours.start_time:
            return False 
        
        if slot.time() > eu_workhours.end_time:
            return False 
        
        return True

    def get_slots(self, person_id: str):
        dao = self.dao
        retrieved_slots = dao.get_slots_by_person(person_id) #TODO person ID? 
        print('retrieved slots', retrieved_slots)
        return retrieved_slots

    def get_all_availabilities(self):
        dao = self.dao
        availabilities = dao.get_all_availabilities()
        print(availabilities)
        return availabilities


    def get_slots_per_person(self, person_id: str, query: AvailabilityQuery) -> list[PersonAvailabilitySlotResponse]:
        available_slots = []
        
        retrieved_slots_from_DB = self.get_slots(person_id)
        print('!!!!! get slots per person', retrieved_slots_from_DB)
        week_beginning = query.start_frame.replace(tzinfo=None)
        week_end = query.end_frame.replace(tzinfo=None)
    
        # for slot in timeframe
        # start time = now
        
            
        for slot in retrieved_slots_from_DB: #TODO need to conver this into a time
            # Sjednocení tzinfo pro DB sloty
            slot_start = slot.start_time.replace(tzinfo=None) if slot.start_time.tzinfo else slot.start_time
            slot_end = slot.end_time.replace(tzinfo=None) if slot.end_time.tzinfo else slot.end_time
            
            # TODO check if above 9 and below 17h
            if slot.start_time < week_beginning:
                continue
            if slot.end_time > week_end:
                continue 

            if not self.is_within_workhours(slot_start) or not self.is_within_workhours(slot_end):
                continue
            # check if not weekend

            
            
            available_slots.append(
                PersonAvailabilitySlotResponse(
                    slot_id=slot.id,
                    person_id=person_id,
                    start=slot.start_time,
                    end=slot.end_time )
            )
            
        return available_slots

    def add_person_availability(self, person_id: str, query: AddPersonAvailabilitySlot) -> PersonAvailabilitySlotResponse:
    
        slot = TimeSlot(
            start_time=query.start,
            end_time=query.end,
            owner_id=person_id,
            owner_type="candidate",
            status="available"
                )

        self.dao.save(entity=slot)
        
