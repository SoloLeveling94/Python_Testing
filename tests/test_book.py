import pytest

import server


@pytest.fixture
def test_client():
    return server.app.test_client()


def test_access_not_real_competition(test_client):
    response = test_client.get('/book/Spring Festival 2022/Simply Li', follow_redirects=True)
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data
