from typing import List, Optional  
from dataclasses import dataclass
from app.models.person import Person

# Entity
@dataclass
class Interviewer(Person):
    person_type: str = "interviewer"

    def __repr__(self):
        return f"interviewer {self.name}"

        
        
    


