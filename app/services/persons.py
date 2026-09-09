from app.dao.person_dao import PersonDao
from app.models.person import Person


class PersonService():

    def __init__(self, p_dao: PersonDao):
        self.p_dao = p_dao

    def get_all_persons(self):
        return self.p_dao.get_all()

    def read_person(self, person_id: str):
        return self.p_dao.get_object_by_id(entity_id=person_id)

    def validate_user_data():
        pass 

    def check_if_user_exists():
        pass 

    def create_person(self, person_data) -> Person: # ADD type which is returned
        person = Person(
            name=person_data.name, 
            email=person_data.email, 
            person_type=person_data.person_type
            )

        self.p_dao.save(person)

        return person

    def delete_person(self, person_id) -> None:
        return self.p_dao.delete(entity_id=person_id)