from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import Optional, TYPE_CHECKING

@dataclass(frozen=True) # Creating the immutable object
class WorkHours:
    id: int
    start_time: time
    end_time: time
    workdays: set[int]