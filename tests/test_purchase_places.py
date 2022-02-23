import pytest

import server


@pytest.fixture
def test_client():
    return server.app.test_client()


@pytest.fixture
def competition_json(monkeypatch):
    monkeypatch.setattr('server.competitions', [
        {
            "name": "Fall Classic 2022",
            "date": "2022-10-22 13:30:00",
            "numberOfPlaces": "10"
        }
    ])


def test_no_enough_points_available(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Iron Temple", "competition": "Spring Festival",
                                                         "places": 8}, follow_redirects=True)
    assert response.status_code == 200, f"You do not have enough points to purchase this places (10)! " \
                                        f"{response.status_code}"


def test_outnumbered_places_required(test_client, competition_json):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Fall Classic 2022",
                                                         "places": 12}, follow_redirects=True)
    assert response.status_code == 200, f"You do not have enough points (4) to purchase this places! " \
                                        f"{response.status_code}"


def test_negative_places_required(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Spring Festival",
                                                         "places": -5}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Enter a positive number to book it!" in response.data


def test_max_12_places_competition(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Spring Festival",
                                                         "places": 13}, follow_redirects=True)
    assert response.status_code == 200, f"You can not book more 12 places in this competition" \
                                        f"{response.status_code}"


def test_updated_points_club(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Spring Festival",
                                                         "places": 10}, follow_redirects=True)
    assert response.status_code == 200
    assert server.clubs[0]['points'] == 3
    assert server.competitions[0]['numberOfPlaces'] == 15



