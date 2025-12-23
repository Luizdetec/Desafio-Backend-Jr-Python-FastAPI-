import pytest


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/auth/register", json={"username": "admin", "password": "123", "role": "admin"})

    response = await client.post("/auth/login", data={"username": "admin", "password": "123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_user_access_denied_to_consoles(client):
    await client.post("/auth/register", json={"username": "user", "password": "123", "role": "user"})
    login = await client.post("/auth/login", data={"username": "user", "password": "123"})
    token = login.json()["access_token"]

    response = await client.post(
        "/consoles/",
        json={"name": "PS5", "company": "Sony"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "FORBIDDEN"