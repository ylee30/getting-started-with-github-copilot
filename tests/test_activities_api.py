def test_get_activities_returns_activity_mapping(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert expected_activity in payload
    assert isinstance(payload[expected_activity]["participants"], list)


def test_signup_adds_new_participant(client, sample_data):
    # Arrange
    activity_name = sample_data["existing_activity"]
    email = sample_data["new_participant"]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_fails_when_participant_already_registered(client, sample_data):
    # Arrange
    activity_name = sample_data["existing_activity"]
    email = sample_data["existing_participant"]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_fails_for_unknown_activity(client, sample_data):
    # Arrange
    activity_name = "Unknown Activity"
    email = sample_data["new_participant"]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant(client, sample_data):
    # Arrange
    activity_name = sample_data["existing_activity"]
    email = sample_data["existing_participant"]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_fails_for_unknown_activity(client, sample_data):
    # Arrange
    activity_name = "Unknown Activity"
    email = sample_data["existing_participant"]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_fails_when_participant_not_registered(client, sample_data):
    # Arrange
    activity_name = sample_data["existing_activity"]
    email = sample_data["new_participant"]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found for this activity"}


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in {302, 307}
    assert response.headers["location"] == expected_location
