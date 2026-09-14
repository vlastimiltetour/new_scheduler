from app.dao.person_dao import PersonDao
from app.models.person import Person


class PersonService():

    def __init__(self, dao: PersonDao):
        self.dao = dao

    def get_all_persons(self):
        return self.dao.get_all()

    def read_person(self, person_id: str):
        return self.dao.get_object_by_id(entity_id=person_id)

    def validate_user_data():
        pass 

    def check_if_user_exists():
        pass 

    def create_person(self, person_data) -> Person: 
        person = Person(
            name=person_data.name, 
            email=person_data.email, 
            person_type=person_data.person_type
            )

        self.dao.create(person)

        return person

    # Merging PUT and PATCH to one update
    def update_person(self, entity_id, changes) -> Person: 

        person = self.read_person(person_id=entity_id)

        if person:
            if hasattr(changes, "model_dump"): 
                # Pydantic v2 model: dump only explicitly provided fields
                changes_dict = changes.model_dump(exclude_unset=True)
        
            elif isinstance(changes, dict): 
                # Raw Python dictionary 
                changes_dict = changes

            for field, value in changes_dict.items():
                setattr(person, field, value)
            

            self.dao.update(person)

        return person

    def delete_person(self, person_id) -> None:
        return self.dao.delete(entity_id=person_id)