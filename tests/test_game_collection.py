import pytest


@pytest.mark.asyncio
async def test_admin_create_console_and_game(client):
    await client.post("/auth/register", json={"username": "admin", "password": "123", "role": "admin"})
    login = await client.post("/auth/login", data={"username": "admin", "password": "123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    console_resp = await client.post("/consoles/", json={"name": "N64", "company": "Nintendo"}, headers=headers)
    console_id = console_resp.json()["data"]["id"]
    assert console_resp.status_code == 200

    game_resp = await client.post("/games/", json={"name": "Zelda", "console_id": console_id}, headers=headers)
    assert game_resp.status_code == 200
    assert game_resp.json()["data"]["console_name"] == "N64"

    list_resp = await client.get("/games/", headers=headers)
    assert len(list_resp.json()["data"]) == 1

    list_by_console = await client.get(f"/consoles/{console_id}/games", headers=headers)
    assert list_by_console.status_code == 200
    assert len(list_by_console.json()["data"]) == 1