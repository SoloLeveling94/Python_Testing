import pytest

import server


@pytest.fixture
def test_client():
    return server.app.test_client()


def test_login_with_display_list(test_client):
    response = test_client.post('/showSummary', data={"email": "john@simplylift.co"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Simply Lift: 13 points" in response.data
    assert b"Iron Temple: 4 points" in response.data
    assert b"She Lifts: 12 points" in response.data

