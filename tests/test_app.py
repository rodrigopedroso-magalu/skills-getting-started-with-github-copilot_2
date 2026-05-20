from urllib.parse import quote


def test_root_redirect(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Soccer Team" in data
    assert isinstance(data["Soccer Team"], dict)


def test_signup_for_activity(client):
    activity_name = "Soccer Team"
    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up student@example.com for {activity_name}"}

    activity_response = client.get("/activities")
    assert "student@example.com" in activity_response.json()[activity_name]["participants"]


def test_duplicate_signup_returns_400(client):
    activity_name = "Soccer Team"
    params = {"email": "student@example.com"}

    first_response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params=params,
    )
    assert first_response.status_code == 200

    duplicate_response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params=params,
    )
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant(client):
    activity_name = "Soccer Team"
    email = "student@example.com"

    signup_response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Removed {email} from {activity_name}"}


def test_remove_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Soccer%20Team/participants",
        params={"email": "missing@example.com"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
