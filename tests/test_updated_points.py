import pytest

import server


@pytest.fixture
def test_client():
    return server.app.test_client()


def test_updated_points_club(test_client):
    response = test_client.post('/purchasePlaces', data={"club": "Simply Lift", "competition": "Spring Festival",
                                                         "places": 10}, follow_redirects=True)
    assert response.status_code == 200
    assert server.clubs[0]['points'] == 3
    assert server.competitions[0]['numberOfPlaces'] == 15