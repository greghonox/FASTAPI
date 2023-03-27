from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_artigos():
    response = client.get("/v1/artigos")
    assert response.status_code == 200