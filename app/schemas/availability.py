from typing import List, Optional  
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

# Read Slots by Person ID
class PersonAvailabilitySlotResponse(BaseModel):
    slot_id: UUID 
    person_id: UUID
    start: datetime
    end: datetime

class AvailabilityRead(BaseModel):
    slot_id: UUID
    start: datetime
    end: datetime

class AddPersonAvailabilitySlot(BaseModel):
    start: datetime
    end: datetime

# Query Slots by Person - leave person ID out
class AvailabilityQuery(BaseModel):
    start_frame: datetime 
    end_frame: datetime
    