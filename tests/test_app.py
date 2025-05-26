from fastapi.testclient import TestClient

from test_infog.app import app

client = TestClient(app)

def test_root_return_ola_mundo():
    client = TestClient(app)

    response  = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}