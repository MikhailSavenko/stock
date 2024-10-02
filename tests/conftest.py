import asyncio
import pytest
from httpx import ASGITransport, AsyncClient

from app.crud.order import order_crud
from app.crud.product import product_crud
from app.main import app
from app.schemas.product import ProductCreate

from app.core.db import Base, get_async_session
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


TEST_DB = BASE_DIR / 'test.db'
SQLALCHEMY_DATABASE_URL = f'sqlite+aiosqlite:///{str(TEST_DB)}'
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)
TestingSessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def override_get_async_session():
    async with TestingSessionLocal() as async_session:
        yield async_session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_session():
    async with TestingSessionLocal() as async_session:
        yield async_session


@pytest.fixture(scope='session')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session')
async def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def test_order(async_session):
    order_test = await order_crud.create(session=async_session)
    yield order_test


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
