from main import app
import pytest
from httpx import AsyncClient
import asyncio

base_url = 'http://127.0.0.1:8080/api/v1/'
url = 'https://practicum.yandex.ru/'
short_id = 'XaUjDbzfiv'


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_url(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post('/', json={'target_url': url})
    assert response.status_code == 201
    data = response.json()
    short_id = data['short_url_id']

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f'/{short_id}')
    assert response.status_code == 307

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f'/{short_id}/target')
    assert response.status_code == 307
    assert response.json() == url

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f'/{short_id}/status')
    assert response.status_code == 200
    assert response.json() == {'clicks': 1}

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.delete(f'/{short_id}')
    assert response.status_code == 200
    assert response.json() == {
        'target_url': 'https://practicum.yandex.ru/',
        'is_active': False
    }


@pytest.mark.asyncio
async def test_ping():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get('/ping')
    assert response.status_code == 200
    assert response.json() == {'status': 'active'}


@pytest.mark.asyncio
async def test_url_list():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post('/shorten', json=[
            {'target_url': url},
            {'target_url': base_url}])
    assert response.status_code == 201
