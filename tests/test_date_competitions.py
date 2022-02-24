import pytest

import server


@pytest.fixture
def test_client():
    return server.app.test_client()


def test_access_forbidden_date_competition(test_client):
    response = test_client.get('/book/Spring Festival/Simply Lift', follow_redirects=True)
    assert response.status_code == 200
    assert b"Choose an another competition. The date has expired!" in response.data


def test_access_date_competition(test_client):
    response = test_client.get('/book/Spring Festival 2022/Simply Lift', follow_redirects=True)
    assert response.status_code == 200
    assert b"Booking for Spring Festival 2022" in response.data
