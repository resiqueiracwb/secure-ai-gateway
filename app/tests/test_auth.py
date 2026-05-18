from fastapi.testclient import (
    TestClient
)

from app.main import app

client = TestClient(app)


def test_login_success():

    response = client.post(
        "/auth/login",
        json={
            "username": "renato",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    def test_login_invalid_password():
        response = client.post(
            "/auth/login",
            json={
                "username": "renato",
                "password": "wrong-password"
            }
        )

        assert response.status_code == 401