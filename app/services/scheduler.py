from typing import List, Optional  # Importujeme potřebné typy
from dataclasses import dataclass
from datetime import datetime, timedelta
from app.models.person import Person
from app.models.interviewer import Interviewer
from app.models.candidate import Candidate
from app.services.availability import Availability
from app.models.timeslot import TimeSlot
from app.models.workhours import WorkHours
from app.models.interview import Interview
from app.dao.person_dao import PersonDao
from app.dao.interview_dao import InterviewDao
from app.dao.timeslot_dao import TimeSlotDao

class InterviewScheduler:
    def schedule(self, availability: Availability, candidate: Candidate, interviewers: Interviewer, interview_duration: int, timeframe, interview_dao=InterviewDao):
        #take candidate and schedule with interviewers 
        #iterate over interviewers
        self.intervew_duration = interview_duration
        all_matching_slots = []
    
        for interviewer in interviewers:  
            interviewer_slots = availability.get_slots_per_person(person=interviewer, slot_duration=interview_duration, timeframe=timeframe)
            candidate_slots = availability.get_slots_per_person(person=candidate, slot_duration=interview_duration,timeframe=timeframe)
            
            matching_slots = [i for i in interviewer_slots if i in candidate_slots]
            
            for slot in matching_slots:
                all_matching_slots.append((slot, interviewer))
        
        if all_matching_slots:
            earliest_slot = self._find_earliest_slot(all_matching_slots)
        
            print('candidate', candidate, type(candidate), "interviewer", interviewer, type(interviewer))
            interview_scheduled = Interview(
                #id=1, # TODO BUG Automatically generate 
                candidate=candidate, 
                interviewer=earliest_slot[1],
                timeslot=earliest_slot[0]
            )
            
            interview_dao.save(interview_scheduled) 

            return interview_scheduled
        
       
        return None
    
    def _find_earliest_slot(self, slot_list): 
        earliest_slot = sorted(slot_list, key=lambda x: x[0])
        
        if earliest_slot:
            return earliest_slot[0]

        return None

