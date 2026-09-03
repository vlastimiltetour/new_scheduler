#This is the DAO layer
import json
import os
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from app.models.timeslot import TimeSlot
from sqlalchemy import text
from app.models.person import Person
from app.models.interviewer import Interviewer
from app.models.candidate import Candidate
import logging
from sqlalchemy.exc import IntegrityError

# Design of the DAO layer
'''
You should pass the whole object when the DAO is writing data.
For save() or update(): Pass the whole object. The DAO needs the data to store it.

For get, delete, or find: Pass the ID only. It’s cleaner, less memory-intensive, and prevents "Object vs. Function" errors.
'''
logger = logging.getLogger(__name__)

class TimeSlotDao:
    def __init__(self, engine):
        self.engine = engine
        self.table =  "timeslot"

    # create
    def save(self, entity: TimeSlot):
        # add a new user to the database

        query = text(f"INSERT INTO {self.table} (ID, START_TIME, END_TIME, OWNER_ID, OWNER_TYPE, STATUS) VALUES (:id, :start_time, :end_time, :owner_id, :owner_type, :status);")

        # engine.begin command commits the record in db, engine.connect will not
        # engine.begin() → auto-commit on success
        try:
            with self.engine.begin() as conn: 
                
                conn.execute(query, {"id": entity.id,
                                            "start_time": entity.start_time, 
                                            "end_time": entity.end_time,
                                            "owner_id": entity.owner_id,
                                            "owner_type": entity.owner_type,
                                            "status": entity.status})

            logger.info(f"Object {entity.id} has been saved into the DB.")
        
        except IntegrityError as e:
            logger.error(f"Object {entity.id} has been already in the DB. Error detail:{e}")

    # read
    def get_object_by_id(self, entity_id: str):
        query = text(f"SELECT * FROM {self.table} WHERE ID =:id")
        
        with self.engine.connect() as conn:
            result = conn.execute(query, {"id": entity_id})            
            result = result.fetchone()
            
            logger.info(f"Object {result} has been retrieved.")
            
            if result:
                return TimeSlot(id=result.id, start_time=result.start_time, end_time=result.end_time, owner_id=result.owner_id, owner_type=result.owner_type, status=result.status)
        
        return None

    # update
    def update(self, entity: TimeSlot):
        query = text(f"""
            UPDATE {self.table}
            SET START_TIME = :start_time,
                END_TIME = :end_time,
                OWNER_ID = :owner_id,
                ONWER_TYPE = :owner_type,
                STATUS = :status,
            WHERE ID = :id;
                     """)
        
        with self.engine.begin() as conn: 
            
            conn.execute(query, {"id": entity.id,
                                           "start_time": entity.start_time, 
                                           "end_time": entity.end_time,
                                           "owner_id": entity.owner_id,
                                           "owner_type": entity.owner_type,
                                           "status": entity.status})

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


    def get_blocked_slots_by_person(self, owner_id: int) -> list[TimeSlot]:
        query = text(f"SELECT * FROM {self.table} WHERE OWNER_ID =:owner_id AND STATUS ='unavailable'")
        blocked_slots = []
        
        with self.engine.begin() as conn:
            result = conn.execute(query, {"owner_id": owner_id})            
            result = result.fetchall()

            
            for row in result:
                slot = TimeSlot(id=row.id, start_time=row.start_time, end_time=row.end_time, owner_id=row.owner_id, owner_type=row.owner_type, status=row.status)
                blocked_slots.append(slot)
            
            logger.info(f"Blocked slots {blocked_slots} has been retrieved.")
        
        return blocked_slots