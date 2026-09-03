#This is the DAO layer
import json
import os
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from app.models.timeslot import TimeSlot


# Design of the DAO layer
'''
You should pass the whole object when the DAO is writing data.
For save() or update(): Pass the whole object. The DAO needs the data to store it.

For get, delete, or find: Pass the ID only. It’s cleaner, less memory-intensive, and prevents "Object vs. Function" errors.
'''

class TimeSlotDao:
    def __init__(self, storage_file: str = "slots.json"):
        self._directory = "interview_scheduler/data" #creation of the path
        self._storage_file = os.path.join(self._directory, storage_file) #combining with the filename

        # Ensure the directory exists so open() doesn't fail
        os.makedirs(self._directory, exist_ok=True)

    def _load_data(self) -> Dict: #this is not ideal, opening up every time 
        if not os.path.exists(self._storage_file):
            return {}
        try:
            with open(self._storage_file, 'r') as f:
                raw_data = json.load(f)
                return raw_data
        except (FileNotFoundError,json.JSONDecodeError):
            return {}
        
    def _update_data(self, data: Dict):
        with open(self._storage_file, 'w') as f:
            json.dump(data, f, indent=4)

    #create & update
    def save(self, object: TimeSlot): #store the pesron type
        data = self._load_data()

        object_dict = asdict(object)

        #convert datetime to isoformat  
        object_dict = self._serialize(object_dict, object)      
        
        #getting ready to update 
        # take the data file, find or create the object.id from TimeSlot and assign object_dict which has been turned into dict 
        data[str(object.id)] = object_dict
        
        self._update_data(data)
        print(f'saved Timeslot {object.id, object.owner_id} succesfully into database')

    #read
    def get_object_by_id(self, object_id: int) -> Optional[TimeSlot]: #finish the data copy TODO 
        data = self._load_data()

        record = data.get(str(object_id))

        if not record:
            return None
        
        return TimeSlot(**record)
    
    #read - list all slots  #TODO this logic should be object_id not person_id - that should be hanlded separately, right? 
    def get_blocked_slots_by_person(self, owner_id: int):  #passing an object
        data = self._load_data()
        result = []

        for record in data.values():
            if record.get("owner_id") == int(owner_id):
                record = self._deserialize(record)
                result.append(TimeSlot(**record))
        return result
    
    #delete
    def delete(self, object_id) -> bool:
        data = self._load_data()
        object_id = str(object_id)

        if object_id in data:
            del data[object_id]        
            self._update_data(data)
            return True
        
        return False
    
    def _deserialize(self, record):
        record_copy = record.copy()
        record_copy['start'] = datetime.fromisoformat(record_copy['start'])
        record_copy['end'] = datetime.fromisoformat(record_copy['end'])

        return record_copy

    def _serialize(self, record, object):
        record["start"] = object.start.isoformat()
        record["end"] = object.end.isoformat()

        return record

