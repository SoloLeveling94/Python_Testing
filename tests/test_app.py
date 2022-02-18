import pytest

import server


@pytest.fixture
def test_client():
    return server.app.test_client()


def test_should_status_code_ok(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_login_with_registered_email(test_client):
    response = test_client.post('/showSummary', data={"email": "john@simplylift.co"}, follow_redirects=True)
    assert response.status_code == 200


def test_login_with_unregistered_email(test_client):
    response = test_client.post('/showSummary', data={"email": "test@xyz.com"}, follow_redirects=True)
    assert response.status_code == 200


def test_no_enough_points_available(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Iron Temple", "competition": "Spring Festival",
                                                         "places": 8}, follow_redirects=True)
    assert response.status_code == 200


def test_outnumbered_places_required(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Spring Festival",
                                                         "places": 13}, follow_redirects=True)
    assert response.status_code == 200


def test_negative_places_required(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Spring Festival",
                                                         "places": -5}, follow_redirects=True)
    assert response.status_code == 200


