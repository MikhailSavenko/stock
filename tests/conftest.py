import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.crud.order import order_crud
from app.core.db import AsyncSessionLocal

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session

@pytest.fixture
async def test_order(async_session):
    order_test = await order_crud.create(session=async_session)
    print(order_test.id)
    yield order_test
    await order_crud.remove(order_test, session=async_session)