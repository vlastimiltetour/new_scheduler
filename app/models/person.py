from typing import List, Optional  
from dataclasses import dataclass, field
from app.models.entity import Entity
from uuid import UUID, uuid4


# Entity
@dataclass
class Person(Entity):
   id: UUID = field(default_factory=uuid4)
   name: str = None
   email: str = None 
   person_type: str = None
   #workhours: object = None



