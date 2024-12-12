from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_exchange_rates_current():
    response = client.get("/exchange-rates/current")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    data = response.json()
    assert len(data) == 30
    assert "currency" in data[0]
    assert "rate" in data[0]

def test_exchange_rates_compare():
    response = client.get("/exchange-rates/compare")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    data = response.json()
    assert len(data) == 30
    assert "currency" in data[0]
    assert "rate" in data[0]
    assert "change" in data[0]


