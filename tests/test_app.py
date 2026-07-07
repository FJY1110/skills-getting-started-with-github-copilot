from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

INITIAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = deepcopy(INITIAL_ACTIVITIES)
    yield
    app_module.activities = deepcopy(INITIAL_ACTIVITIES)


@pytest.fixture
def client():
    return TestClient(app_module.app)


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_signup_and_unregister_flow(client):
    signup_response = client.post(
        "/activities/Basketball Team/signup?email=test@mergington.edu"
    )
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == (
        "Signed up test@mergington.edu for Basketball Team"
    )

    unregister_response = client.delete(
        "/activities/Basketball Team/unregister?email=test@mergington.edu"
    )

    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == (
        "Unregistered test@mergington.edu from Basketball Team"
    )


def test_signup_rejects_duplicate_participant(client):
    client.post("/activities/Basketball Team/signup?email=test@mergington.edu")

    duplicate_response = client.post(
        "/activities/Basketball Team/signup?email=test@mergington.edu"
    )

    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == (
        "Student is already signed up for this activity"
    )


def test_unregister_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Basketball Team/unregister?email=ghost@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
