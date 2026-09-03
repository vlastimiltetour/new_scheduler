#This is the DAO layer
import json
import os
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from app.models.person import Person
from app.models.candidate import Candidate
from app.models.interviewer import Interviewer
from app.models.interview import Interview

# Design of the DAO layer
'''
You should pass the whole object when the DAO is writing data.
1: For save() or update(): Pass the whole object. The DAO needs the data to store it.
2: For get, delete, or find: Pass the ID only. It’s cleaner, less memory-intensive, and prevents "Object vs. Function" errors.
'''

class InterviewDao:
    def __init__(self, storage_file: str = "interviews.json"):
        self._directory = "interview_scheduler/data" #creation of the path
        self._storage_file = os.path.join(self._directory, storage_file) #combining with the filename

        # Ensure the directory exists so open() doesn't fail
        os.makedirs(self._directory, exist_ok=True)

    def _load_data(self) -> Dict: #thi is not ideal, opening up every time 
        if not os.path.exists(self._storage_file):
            return {}
        try:
            with open(self._storage_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError,json.JSONDecodeError):
            return {}
        
    def _update_data(self, data: Dict):
        with open(self._storage_file, 'w') as f:
            json.dump(data, f, indent=4)

    #create & update
    def save(self, object: Interview): #store the pesron type
        data = self._load_data()

        object_dict = asdict(object)
        
        print("object_dict", object_dict)

        data[str(object.id)] = object_dict
        
        self._update_data(data)
        print(f'saved {object.name} succesfully into database')

    #read
    def get_object_by_id(self, object_id: int) -> Optional[Interview]:  #finish the data copy TODO
        data = self._load_data()
    
        record = data.get(str(object_id))

        if not record:
            return None
        
        cls_name = record.pop("cls_type", "Person")
        cls = self.TYPE_MAP.get(cls_name, Person)

        return cls(**record)
    
    #read
    def list_all(self) -> List[Person]:  #finish the data copy TODO
        data = self._load_data()
        result = []

        for value in data.values():
            cls_name = value.pop("cls_type", "Person")
            cls = self.TYPE_MAP.get(cls_name, Person)            
            result.append(cls(**value))
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
    
