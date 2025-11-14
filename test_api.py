import pytest
from app import app as flask_app  

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Flask API running" in r.get_json()["message"]

def test_status(client):
    r = client.get("/status")
    assert r.status_code == 200
    assert r.get_json() == {"message": "ok"}

def test_sum_success_integers(client):
    r = client.get("/sum?a=5&b=7")
    assert r.status_code == 0 or r.status_code == 200  
    assert r.get_json()["sum"] == 12

def test_sum_success_floats(client):
    r = client.get("/sum?a=2.5&b=1.25")
    assert r.status_code == 200
    assert abs(r.get_json()["sum"] - 3.75) < 1e-9

def test_sum_missing_param(client):
    r = client.get("/sum?a=5")
    assert r.status_code == 400
    assert "error" in r.get_json()

def test_sum_invalid_param(client):
    r = client.get("/sum?a=foo&b=2")
    assert r.status_code == 400
    assert "error" in r.get_json()
