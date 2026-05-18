from fastapi.testclient import (
    TestClient
)

from app.main import app

client = TestClient(app)


def test_ai_prompt_requires_auth():

    response = client.post(
        "/ai/prompt",
        json={
            "prompt": "hello",
            "provider": "openai"
        }
    )

    assert response.status_code == 401


def test_ai_prompt_success():
    login_response = client.post(
        "/auth/login",
        json={
            "username": "renato",
            "password": "123456"
        }
    )

    token = login_response.json()[
        "access_token"
    ]

    response = client.post(
        "/ai/prompt",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "prompt": "hello",
            "provider": "openai"
        }
    )

    assert response.status_code == 200
