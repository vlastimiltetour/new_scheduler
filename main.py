from typing import List, Optional  # Importujeme potřebné typy
from dataclasses import dataclass
from datetime import datetime, timedelta, time
from app.services.availability import Availability
from app.models.timeslot import TimeSlot
from app.services.scheduler import InterviewScheduler
from app.dao.person_dao import PersonDao
from app.dao.interview_dao import InterviewDao
from app.dao.timeslot_dao import TimeSlotDao
from app.dao.orm import start_mappers
from app.models.person import Person
from app.models.workhours import WorkHours
from app.models.candidate import Candidate
from app.models.interviewer import Interviewer
from app.dao.database import engine


def main() -> None: 
    db_engine = engine()

    person_dao = PersonDao(engine=db_engine)
    ts_dao = TimeSlotDao(engine=db_engine)
    int_dao = InterviewDao(engine=db_engine)


    # Data Preparation
    eu_workhours = WorkHours(
        id=1, 
        start_time=time(9, 0), 
        end_time=time(16, 0), 
        workdays={0, 1, 2, 3, 4}
    )


    # Data Creation 
    alan = Candidate(name="Alan Harper", email="alan@harper.com", person_type="candidate")
    person_dao.save(alan)
    
    
    
    carl = Interviewer(name="Carl Uberinterviewer", email="carl@everpure.com", person_type="interviewer")
    person_dao.save(carl)

    ts_dao.save(TimeSlot(start_time=datetime(2026,4,6,9,00), end_time=datetime(2026, 4, 6, 13,00), owner_id=carl.id, owner_type="interviewer",status="unavailable"))
    
    johnny = Interviewer(name="Johnny Cage", email="johnny@cage", person_type="interviewer")
    person_dao.save(johnny)
    ts_dao.save(TimeSlot(start_time=datetime(2026,4,6,9,00), end_time=datetime(2026, 4, 6, 11,00), owner_id=johnny.id, owner_type="interviewer",status="unavailable"))

    #person_dao.delete(entity_id=7)
    #person_dao.delete(entity_id=8)
    #person_dao.delete(entity_id=6)

    # Try to call data
    #carl = person_dao.get_object_by_id(entity_id=6)
    #alan = person_dao.get_object_by_id(entity_id=7)


    availability_service = Availability(now=datetime(2026, 4, 6, 9, 0), 
                                        calendar_period=datetime(2026, 12, 31, 6,0), 
                                        workhours=eu_workhours, 
                                        timeslotdao=ts_dao)

    availability = availability_service.get_slots_per_person(person=johnny, 
                                              slot_duration=60, 
                                              timeframe=datetime(2026, 4, 10, 19,0))
    print('johny availability', availability)
    scheduler = InterviewScheduler()
    scheduled_interview = scheduler.schedule(availability=availability_service, 
                                   candidate=alan,
                                   interviewers=[carl, johnny],
                                   interview_duration=60,
                                   timeframe=datetime(2026, 4, 10, 19,0),
                                   interview_dao=int_dao)
    
    

    # PRINTING 
    print(f"\n--- Printing a very nice beautiful output ---")
    #print(person_dao.get_object_by_id(entity_id=7))
    print('lenght of availability', len(availability))
    for slot in availability[:5]:
        print(slot)

    print('this is scheduled interview', scheduled_interview)
        
if __name__ == "__main__":
    main()
    