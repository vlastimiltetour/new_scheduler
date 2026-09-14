from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.persons import PersonCreate, PersonRead
from app.dao.person_dao import PersonDao
from app.models.person import Person
from app.services.persons import PersonService
from app.dao.database import engine


def get_availability_service():
    pass 