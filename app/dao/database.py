"""
Soubor database.py slouží jako nízkoúrovňový most k PostgreSQL.

Jeho úkolem je vytvořit Engine a inicializovat ORM mapování.
"""

import os

from sqlalchemy import create_engine
from app.dao.orm import start_mappers, metadata


APP_ENV = os.getenv("APP_ENV", "local")

DATABASE_URL = os.environ["DATABASE_URL"]


def engine():
    db_engine = create_engine(DATABASE_URL)

    start_mappers()
    metadata.create_all(bind=db_engine)

    return db_engine