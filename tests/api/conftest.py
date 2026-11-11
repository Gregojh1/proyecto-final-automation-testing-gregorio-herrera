import pytest
import requests

@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    session.base_url = "https://reqres.in/api"
    return session