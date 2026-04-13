import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.mark.parametrize("endpoint", [
    "/posts",
    "/comments",
    "/users"
])
def test_public_endpoints(endpoint):
    response = requests.get(f"{BASE_URL}{endpoint}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)