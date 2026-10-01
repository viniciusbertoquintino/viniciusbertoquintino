from datetime import datetime, timedelta

import jwt
import pytest

from app.core.config import settings


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "2.1.0"}


@pytest.mark.parametrize(
    ("email", "role", "name"),
    [
        ("admin@acme.com", "admin", "Rafael Costa"),
        ("user@acme.com", "user", "Ana Lima"),
    ],
)
def test_login_returns_bearer_token(client, email, role, name):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "demo1234"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["user"] == {"email": email, "name": name, "role": role}
    payload = jwt.decode(body["access_token"], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == email
    assert payload["role"] == role


def test_login_rejects_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@acme.com", "password": "errada"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"


def test_login_rejects_unknown_user(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "ninguem@acme.com", "password": "demo1234"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"


def test_login_requires_email_and_password(client):
    response = client.post("/api/v1/auth/login", json={})

    assert response.status_code == 422


def test_me_returns_token_payload(client):
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@acme.com", "password": "demo1234"},
    )
    token = login.json()["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    body = response.json()
    assert body["sub"] == "admin@acme.com"
    assert body["role"] == "admin"


def test_me_requires_bearer_token(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 403


def test_me_rejects_invalid_token(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido"


def test_me_rejects_expired_token(client):
    token = jwt.encode(
        {
            "sub": "admin@acme.com",
            "role": "admin",
            "exp": datetime.utcnow() - timedelta(minutes=5),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Token expirado"
