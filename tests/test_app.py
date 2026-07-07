from fastapi.testclient import TestClient

from src.app import app


def test_unregister_participant_from_activity():
    client = TestClient(app)

    signup_response = client.post(
        "/activities/Basketball Team/signup?email=test@mergington.edu"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        "/activities/Basketball Team/unregister?email=test@mergington.edu"
    )

    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == (
        "Unregistered test@mergington.edu from Basketball Team"
    )
