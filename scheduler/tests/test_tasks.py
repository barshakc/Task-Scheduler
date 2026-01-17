from datetime import datetime, timezone

def get_token(client):
    username = "testuser"
    password = "testpass"

    response = client.post("/register", json={"username": username, "password": password})
    assert response.status_code == 200

    login_resp = client.post("/login", data={"username": username, "password": password})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_task(client):
    headers = get_token(client)

    task_payload = {
        "name": "pytest_task",
        "description": "Test task",
        "schedule_type": "once",
        "schedule_value": datetime.now(timezone.utc).isoformat(),
        "max_runs": 1,
        "payload": {
            "recipient": "test@example.com",
            "subject": "Test",
            "message": "Test message"
        }
    }

    response = client.post("/tasks", json=task_payload, headers=headers)
    assert response.status_code in [200, 201]


