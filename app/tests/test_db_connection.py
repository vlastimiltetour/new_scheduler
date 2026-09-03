import pytest
import psycopg
from sqlalchemy import text 
from testcontainers.postgres import PostgresContainer
# source: https://pytest-test-categories.readthedocs.io/en/latest/examples/container-testing.html


def test_can_connect_and_query(postgres_container):
    # Spustíme Postgres 16 v Dockeru
    
    # Získáme připojovací řetězec
    db_url = postgres_container.get_connection_url(driver=None)
    
    # Zkusíme se reálně připojit
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 'Architektura funguje!'")
            msg = cur.fetchone()[0]
            print(f"\n[DOCKER]: {msg}")
            assert msg == "Architektura funguje!"

@pytest.mark.medium
def test_creates_person_in_database(postgres_container, sample_person):
    db_url = postgres_container.get_connection_url(driver=None)

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cursor:

            # Create table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS person (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL
                )
            """)
            
            # Insert person
            sql_command =  "INSERT INTO person (name, email) VALUES (%s, %s) RETURNING id"
            cursor.execute(sql_command, (sample_person.name, sample_person.email))

            person_id = cursor.fetchone()[0]
            conn.commit()

            # Verify
            cursor.execute("SELECT name FROM person WHERE id = %s", (person_id,))
            name = cursor.fetchone()[0]

            cursor.execute("SELECT email FROM person WHERE id =%s", (person_id,))
            email = cursor.fetchone()[0]

            assert name == "Sample_Person"
            assert email == "person@person.com"

            cursor.close()
            conn.close()


'''
Unit testy (rychlé) označíš @pytest.mark.fast.
Integrační testy (s Dockerem) označíš @pytest.mark.medium.
End-to-end testy (pomalé) označíš @pytest.mark.slow.
'''
@pytest.mark.medium
def test_sqlalchemy_operations(sql_alchemy_postgres_engine):
    with sql_alchemy_postgres_engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                price DECIMAL(10, 2)
            )
        """))
        conn.execute(
            text("INSERT INTO products (name, price) VALUES (:name, :price)"),
            {"name": "Widget", "price": 19.99},
        )
        conn.commit()

        result = conn.execute(text("SELECT price FROM products WHERE name = :name"), {"name": "Widget"})
        price = result.scalar()

    assert float(price) == 19.99