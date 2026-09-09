from fastapi import APIRouter
from app.api.v1.routers import persons

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(persons.router, prefix="/persons", tags=["Persons"])
#api_router.include_router(availability.router)
#api_router.include_router(interviews.router)