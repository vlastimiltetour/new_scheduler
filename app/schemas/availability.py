from typing import List, Optional  
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

class PersonAvailabilitySlotResponse(BaseModel):
    start: datetime
    end: datetime

class AddPersonAvailabilitySlot(BaseModel):
    start: datetime
    end: datetime

class AvailabilityQuery(BaseModel):
    slot_duration: int = 60 
    start_frame: datetime | None = datetime(2026,4,19,9,0) 
    end_frame: datetime | None = datetime(2026,4,20,17,0)
    #workhours: WorkHours | None = eu_workhours