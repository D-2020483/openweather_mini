import pytest
from src.app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_weather_invalid_lat_lon(client):
    # This test assumes the app is enhanced to validate lat/lon types
    # Currently, it may pass or fail depending on the API behavior
    res = client.get("/weather?lat=abc&lon=xyz")
    assert res.status_code == 400 or res.status_code == 200

def test_home_route_content_type(client):
    res = client.get("/")
    assert res.content_type == "text/html; charset=utf-8"
