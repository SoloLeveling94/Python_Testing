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
            "numberOfPlaces": "2"
        },
        {
            "name": "Winter Classic 2022",
            "date": "2022-12-25 13:30:00",
            "numberOfPlaces": "3"
        },
        {
            "name": "Summer Classic 2022",
            "date": "2022-6-25 13:30:00",
            "numberOfPlaces": "30",
            "Simply Lift": "2"
        }
    ])


def test_no_enough_points_available(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Iron Temple", "competition": "Spring Festival",
                                                         "places": 8}, follow_redirects=True)
    assert response.status_code == 200, f"You do not have enough points to purchase this places (4) ! " \
                                        f"{response.status_code}"
    # assert response.status_code == 200
    # assert b"You do not have enough points (4) to purchase this places!" in response.data


def test_outnumbered_places_required(test_client, competition_json):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Winter Classic 2022",
                                                         "places": 4}, follow_redirects=True)
    assert response.status_code == 200, f"You can not purchase more than the number of places available (3)!" \
                                        f"{response.status_code}"


def test_negative_places_required(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Spring Festival",
                                                         "places": -5}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Enter a positive number to book it!" in response.data


def test_not_number_places_required(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Spring Festival",
                                                         "places": "abc"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Enter a number!" in response.data


def test_max_12_places_competition(test_client, competition_json):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Summer Classic 2022",
                                                         "places": 4}, follow_redirects=True)
    # assert response.status_code == 200, f"You can not book more 12 places in this competition" \
    #                                     f"{response.status_code}"
    assert response.status_code == 200
    assert b"You can not book more than 2 places in this competition" in response.data



