from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import Optional, TYPE_CHECKING
from app.models.entity import Entity
from app.models.person import Person

# TimeSlot could be understood as Value Object, but in this app, it's conceptualized as Entity - as bound to person - it has a lifecycle (different states) and identity (referencing other objects)
# We expect calendar to be open at working hours; timeslot represents unavailable / blocked slots.
@dataclass
class TimeSlot(Entity):
    start_time: datetime 
    end_time: datetime 
    owner_id: Person
    owner_type: str 
    status: str