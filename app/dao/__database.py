"""
Soubor database.py slouží jako nízkoúrovňový most k PostgreSQL.

Jeho úkolem je vytvořit Engine a inicializovat ORM mapování.
"""

import os

from sqlalchemy import create_engine
from app.dao.orm import start_mappers, metadata

# 0. App Environment
APP_ENV = os.getenv("APP_ENV", "production")

# 1. Konfigurace (ideálně z proměnných prostředí nebo konfiguračního souboru)
if APP_ENV == "production": 
    DATABASE_URL = os.environ["DATABASE_URL"]

elif APP_ENV == "local":
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "DB")

    # Sestavení URL adresy (Postgres vyžaduje ovladač psycopg2)
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

else:
    pass 

# 2. Vytvoření Engine

def engine():
    db_engine = create_engine(DATABASE_URL)

    start_mappers()
    metadata.create_all(bind=db_engine)

    return db_engine