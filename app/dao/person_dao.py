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
from sqlalchemy import text
import logging
from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)
# Design of the DAO layer
'''
You should pass the whole object when the DAO is writing data.
For save() or update(): Pass the whole object. The DAO needs the data to store it.

For get, delete, or find: Pass the ID only. It’s cleaner, less memory-intensive, and prevents "Object vs. Function" errors.
'''

class PersonDao:
    def __init__(self, engine):
        self.engine = engine
        self.table =  "person"
    
    # create
    def save(self, entity: Person): 
        
        if self.get_by_email(entity.email):
            logger.error(f"Object {entity.email} been already in the DB.")
            return False

        query = text(f"INSERT INTO {self.table} (ID, NAME, EMAIL, PERSON_TYPE) VALUES (:id, :name, :email, :person_type);")

        # engine.begin command commits the record in db, engine.connect will not
        # engine.begin() → auto-commit on success

        # TODO check if email is there already;
        try:
            with self.engine.begin() as conn: 
                
                conn.execute(query, {"id": entity.id,
                                            "name": entity.name, 
                                            "email": entity.email,
                                            "person_type": entity.person_type})

            logger.info(f"Object {entity.name} has been saved into the DB.")

        except IntegrityError as e:
            logger.error(f"Object {entity.name} been already in the DB {e}.")
        
    # read
    def get_object_by_id(self, entity_id: str):
        query = text(f"SELECT * FROM {self.table} WHERE ID =:id")
        
        with self.engine.connect() as conn:
            result = conn.execute(query, {"id": entity_id})            
            result = result.fetchone()
            
            logger.info(f"Object {result} has been retrieved.")
            
            if result:
                return Person(id=result.id, name=result.name, email=result.email, person_type=result.person_type)
        
        return None

    def get_by_email(self, email: str):
        query = text(f"SELECT * FROM {self.table} WHERE EMAIL =:email")
        
        with self.engine.connect() as conn:
            result = conn.execute(query, {"email": email})            
            result = result.fetchone()
            
            logger.info(f"User with email {result} has been already in the database.")
            
            if result:
                return True
        
        return False

    # update
    def update(self, entity: Person | Interviewer | Candidate):
        query = text(f"""
            UPDATE {self.table}
            SET NAME = :name, 
                EMAIL = :email,
                PERSON_TYPE = :person_type
            WHERE ID = :id;
                     """)

        with self.engine.begin() as conn: 
            
            conn.execute(query, {"id": entity.id,
                                           "name": entity.name, 
                                           "email": entity.email,
                                           "person_type": entity.person_type})

        logger.info(f"Object {entity.name} in the DB has been updated.")

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

