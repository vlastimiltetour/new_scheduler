from typing import List, Optional  
from dataclasses import dataclass
from app.models.person import Person

# Candidate is a clear Entity
@dataclass
class Candidate(Person):
    person_type: str = "candidate"

    def __repr__(self):
        return f"candidate {self.name}"
