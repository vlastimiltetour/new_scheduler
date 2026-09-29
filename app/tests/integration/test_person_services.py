import pytest 
from unittest.mock import MagicMock
from typing import List, Optional  # Importujeme potřebné typy



# Commands to run the test
# python3 -m pytest app/tests/integration/test_person_services.py
# python3 -m pytest app/tests/integration/test_person_services.py -vv

# Specific test
# python3 -m pytest app/tests/api/test_api.py::test_get_persons -vv

def test_postgres(postgres_container):
    print("CONTAINER:", postgres_container.get_connection_url())

