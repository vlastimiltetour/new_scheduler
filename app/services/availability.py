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

eu_workhours = WorkHours(
        id=1, 
        start_time=time(9, 0), 
        end_time=time(16, 0), 
        workdays={0, 1, 2, 3, 4}
    )

class AvailabilityService:
    def __init__(self, dao: TimeSlotDao):
        # get slots from a calendar
        self.dao = dao # DAO dependency injection 
    
        # get holidays TODO

    def truncate_to_whole_hours(self):
        self.now = self.start_frame.replace(minute=0, second=0, microsecond=0)
        return self.now

    def is_within_workhours(self, slot):
        if slot.weekday() not in self.workhours.workdays:
            return False 
        
        if slot.time() < self.workhours.start_time:
            return False 
        
        if slot.time() > self.workhours.end_time:
            return False 
        
        return True

    def get_unavailable_slots(self, person_id: str):
        dao = self.dao
        retrieved_slots = dao.get_blocked_slots_by_person(person_id) #TODO person ID? 
        print('retrieved slots', retrieved_slots)
        return retrieved_slots

    def get_slots_per_person(self, person_id: str, query: AvailabilityQuery) -> list[PersonAvailabilitySlotResponse]:
        available_slots = []
        blocked_slots = self.get_unavailable_slots(person_id)
        duration = timedelta(minutes=query.slot_duration) 
        slots_begining = query.start_frame
        # for slot in timeframe
        # start time = now
        while slots_begining < query.end_frame:
            # iterate and check    
            # if slot in calendar
                
            #slots_begining += duration 
            #continue #continue to check other conditions
            # if slot in workhours
           
            # if slot not blocked
            for slot in blocked_slots: #TODO need to conver this into a time
                
                if slot.start_time <= slots_begining and slots_begining < slot.end_time:
                    
                    slots_begining += duration #TODO this adds only slot duration, I need this to be more flexible; 
                    break # break as I won't check any other condition   # <--- "found a problem! Skip the 'else' and don't add this time."
            
            # append 
            else:
                # <--- "checked everything and found NO problems."
                available_slots.append(
                    PersonAvailabilitySlotResponse(
                        start=slots_begining,
                        end=slots_begining + duration)
                )
                slots_begining += duration
                
        return available_slots

    def add_person_availability(self, person_id: str, query: AddPersonAvailabilitySlot) -> PersonAvailabilitySlotResponse:
        

        slot = TimeSlot(
            start_time=query.start,
            end_time=query.end,
            owner_id=person_id,
            owner_type="candidate",
            status="unavailable"
                )

        self.dao.save(entity=slot)
        return PersonAvailabilitySlotResponse(start=query.start_time,end=query.end)
