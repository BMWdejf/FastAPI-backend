from fastapi.testclient import TestClient
from app.core.main import app

client = TestClient(app)

def test_products():
    response = client.get("/products")
    assert response.status_code == 200
    # Waiting for list of products
    assert isinstance(response.json(), list)
    # How will get json data - structure of list
    if response.json():
        assert "fx_id" in response.json()[0]
        assert "code" in response.json()[0]
        assert "name" in response.json()[0]
        assert "link" in response.json()[0]

def test_product():
    pass
