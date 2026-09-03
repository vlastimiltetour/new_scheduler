from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, DateTime
from sqlalchemy.orm import registry, clear_mappers
from app.models.person import Person
from app.models.candidate import Candidate
from app.models.interviewer import Interviewer
from app.models.interview import Interview
from app.models.timeslot import TimeSlot
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
# In this approach, I hold the models in clean Python classes, and solve the sql alchemy connection via Imperative Mapping

metadata = MetaData() # Holds the metadata info about all tables
mapper_registry = registry()

person_table = Table(
    "person",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(50)),
    Column("email", String(50)),
    Column("person_type", String(20)),
)

timeslot_table = Table(
    "timeslot",
    metadata, 
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("start_time", DateTime),
    Column("end_time", DateTime),
    Column("owner_id", UUID(as_uuid=True), ForeignKey("person.id")),
    Column("owner_type", String(20)),
    Column("status", String(20))
)

interview_table = Table(
    "interview",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("candidate", UUID(as_uuid=True), ForeignKey("person.id"), nullable=False),
    Column("interviewer", UUID(as_uuid=True), ForeignKey("person.id"), nullable=False),
    Column("timeslot", DateTime),
)

# Central map function 
def start_mappers():
    clear_mappers()
    #if not mapper_registry.mappers:
    mapper_registry.map_imperatively(Person, person_table, polymorphic_on=person_table.c.person_type)
    mapper_registry.map_imperatively(Candidate, inherits=Person,polymorphic_identity="candidate")
    mapper_registry.map_imperatively(Interviewer, inherits=Person,polymorphic_identity="interviewer")
    mapper_registry.map_imperatively(TimeSlot, timeslot_table)

    mapper_registry.map_imperatively(
        Interview,
        interview_table,
        properties={
            # We map the Python attribute 'candidate' to a relationship,
            # NOT directly to the 'candidate_id' column.
            "candidate_id": relationship(
                Candidate, 
                primaryjoin=interview_table.c.candidate == person_table.c.id,
                post_update=True # Helpful if you have circular dependencies
            ),
            "interviewer_id": relationship(
                Interviewer, 
                primaryjoin=interview_table.c.interviewer == person_table.c.id
            ),
        }
    )