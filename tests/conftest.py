import pytest
from fastapi.testclient import TestClient

from test_infog.app import app


@pytest.fixture
def client():
    return TestClient(app)
