'''Soubor database.py slouží jako nízkoúrovňový most k PostgreSQL. 
Jeho úkolem je vytvořit Engine (stroj, který spravuje připojení) a Session (objekt, přes který tvá DAO vrstva reálně posílá dotazy).'''

# https://medium.com/@romanbessouat/deploy-and-access-a-postgres-dabatase-using-docker-and-sqlalchemy-d06de37079f8

import os
from sqlalchemy import create_engine
from app.dao.orm import start_mappers, metadata

# 1. Konfigurace (ideálně z proměnných prostředí nebo konfiguračního souboru)
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "DB")

# Sestavení URL adresy (Postgres vyžaduje ovladač psycopg2)
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 2. Vytvoření Engine
def engine():
    engine = create_engine(DATABASE_URL)

    start_mappers() # Init ORM mappers
    metadata.create_all(bind=engine) # Creates the tables

    return engine