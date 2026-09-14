from typing import List, Optional  
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class PersonCreate(BaseModel):
   name: str
   email: EmailStr
   person_type: str

class PersonRead(PersonCreate):
   id: UUID

   class Config:
        from_attributes = True

class PersonReplace(BaseModel):
   name: str
   email: EmailStr
   person_type: str

class PersonPatch(BaseModel):
   name: str | None = None
   email: EmailStr | None = None
   person_type: str | None = None