from httpx import AsyncClient


async def test_create_comic(client: AsyncClient, save_data: dict) -> None:
    data = {
        "title": "Test_1",
        "author": "Test_1",
    }
    response = await client.post(url="/api/comics/", json=data)
    assert response.status_code == 201, response.text
    response_data = response.json()
    assert response_data["title"] == "Test_1"
    assert response_data["author"] == "Test_1"
    assert response_data["rating"] == 0
    save_data["comic_id"] = response_data["id"]


async def test_create_rating(client: AsyncClient, save_data: dict) -> None:
    comic_id = save_data["comic_id"]
    data = {
        "comic_id": comic_id,
        "user_id": 1,
        "value": 5,
    }
    response = await client.post(url="/api/ratings/", json=data)
    assert response.status_code == 201, response.text


async def test_read_comic(client: AsyncClient, save_data: dict) -> None:
    comic_id = save_data["comic_id"]
    response = await client.get(url=f"/api/comics/{comic_id}/")
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data["rating"] == 5


async def test_add_new_rating(client: AsyncClient, save_data: dict) -> None:
    comic_id = save_data["comic_id"]
    data = {
        "comic_id": comic_id,
        "user_id": 2,
        "value": 3,
    }
    response = await client.post(url="/api/ratings/", json=data)
    assert response.status_code == 201, response.text


async def test_read_avg_rating(client: AsyncClient, save_data: dict) -> None:
    comic_id = save_data["comic_id"]
    response = await client.get(url=f"/api/ratings/{comic_id}/rating/")
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data == 4
