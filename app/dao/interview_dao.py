#This is the DAO layer
import json
import os
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from app.models.timeslot import TimeSlot
from app.models.person import Person
from app.models.interviewer import Interviewer
from app.models.candidate import Candidate
from app.models.interview import Interview
from sqlalchemy import text
import logging
from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)

# Design of the DAO layer
'''
You should pass the whole object when the DAO is writing data.
1: For save() or update(): Pass the whole object. The DAO needs the data to store it.
2: For get, delete, or find: Pass the ID only. It’s cleaner, less memory-intensive, and prevents "Object vs. Function" errors.
'''
''' id: int
    candidate: Candidate
    interviewer: Interviewer
    timeslot: TimeSlot
'''
class InterviewDao: 
    def __init__(self, engine):
        self.engine = engine
        self.table =  "interview"

    # create
    def save(self, entity: Interview):
        # add a new user to the database

        query = text(f"INSERT INTO {self.table} (ID, CANDIDATE, INTERVIEWER, TIMESLOT) VALUES (:id, :candidate, :interviewer, :timeslot);")

        # engine.begin command commits the record in db, engine.connect will not
        # engine.begin() → auto-commit on success
        try:
            with self.engine.begin() as conn: 
                
                conn.execute(query, {"id": entity.id,
                                            "candidate": entity.candidate.id, 
                                            "interviewer": entity.interviewer.id,
                                            "timeslot": entity.timeslot})

            logger.info(f"Object {entity.id} has been saved into the DB.")
        
        except IntegrityError as e:
            logger.error(f"Object {entity.id} been already in the DB {e}.")

        
    # read
    def get_object_by_id(self, entity_id: str):
        query = text(f"SELECT * FROM {self.table} WHERE ID =:id")
        
        with self.engine.connect() as conn:
            result = conn.execute(query, {"id": entity_id})            
            result = result.fetchone()
            
            logger.info(f"Object {result} has been retrieved.")
            
            if result:
                return Interview(id=result.id, candidate=result.candidate, interviewer=result.interviewer, timeslot=result.timeslot)
        
        return None

    # update
    def update(self, entity: Interview):
        query = text(f"""
            UPDATE {self.table}
            SET CANDIDATE = :candidate, 
                INTERVIEWER = :interviewer,
                TIMESLOT = :timeslot
            WHERE ID = :id;
                     """)
        
        with self.engine.begin() as conn: 
            
             conn.execute(query, {"id": entity.id,
                                           "candidate": entity.candidate, 
                                           "interviewer": entity.interviewer,
                                           "timeslot": entity.timeslot})

        logger.info(f"Object {entity.id} in the DB has been updated.")

    # delete 
    def delete(self, entity_id: str):
        query = text(f"DELETE FROM {self.table} WHERE ID =:id")
    
        with self.engine.begin() as conn:
            result = conn.execute(query, {"id": entity_id})            
            
            if result.rowcount > 0:
                logger.info(f"Object {entity_id} has been deleted.")
                return True
            else:
                logger.info(f"Object {entity_id} has not been deleted.")
                return False

