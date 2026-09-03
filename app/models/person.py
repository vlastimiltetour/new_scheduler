from typing import List, Optional  
from dataclasses import dataclass
from app.models.entity import Entity

# Entity
@dataclass
class Person(Entity):
   name: str = None
   email: str = None 
   person_type: str = None
   #workhours: object = None



