import pytest
from httpx import ASGITransport, AsyncClient

from app.crud.order import order_crud
from app.crud.product import product_crud
from app.main import app
from app.schemas.product import ProductCreate

from .db_test import AsyncSessionLocal


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
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
    yield order_test
    await order_crud.remove(order_test, session=async_session)


@pytest.fixture
async def test_product(async_session):
    obj_in = ProductCreate(
        name='Product A',
        description='description_test',
        cost=333.33,
        quantity=5,
    )
    product_test = await product_crud.create(
        obj_in=obj_in, session=async_session
    )
    yield product_test
