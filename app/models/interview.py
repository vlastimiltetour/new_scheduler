from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import Optional, TYPE_CHECKING
from app.models.interviewer import Interviewer
from app.models.candidate import Candidate
from app.models.timeslot import TimeSlot
from app.models.entity import Entity

# This is a clear aggregate 
@dataclass
class Interview(Entity):
    candidate: Candidate
    interviewer: Interviewer
    timeslot: datetime # TODO solve how to link to TimeSlot object which has unique owner

    def __str__(self):
        return f"The interview betweeen {self.candidate} and interviewer {self.interviewer} will take place on {self.timeslot}."

