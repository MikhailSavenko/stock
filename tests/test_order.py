import pytest
from sqlalchemy import select

from app.api.exeptions import NotFound
from sqlalchemy.orm import selectinload

from app.models import Product, Order

@pytest.mark.anyio
async def test_get_all_orders(async_client):
    """Тест: Получение Списка объектов при GET /orders"""
    response = await async_client.get('/orders/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_one_order(async_client, test_order):
    """Тест: Получение объекта по id: GET orders/id"""
    response = await async_client.get(f'/orders/{test_order.id}')
    assert response.status_code == 200
    assert response.json()['id'] == test_order.id
    assert response.json()['status'] == 'in_process'
    assert isinstance(response.json()['order_item'], list)


@pytest.mark.anyio
async def test_get_404_order_id(async_client):
    """Тест: 404 ошибка при GET к несуществующему orders/id"""
    response = await async_client.get('/orders/66666666')
    assert pytest.raises(NotFound)
    assert response.status_code == 404


async def get_order_with_items(order_id, session):
    query = select(Order).options(selectinload(Order.order_item)).where(Order.id == order_id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_product(obj_id, session):
    query = select(Product).where(Product.id == obj_id)
    result = await session.execute(query)
    return result.scalars().first()

@pytest.mark.anyio
async def test_post_order(async_client, test_product, async_session):
    """Тест: Создане заказа"""
    order_data = {
        'order_item': [{"product_id": test_product.id, "item_quantity": 1}]
    }
    response = await async_client.post('/orders/', json=order_data)
    order_id = response.json()['id']
    data =  await get_order_with_items(order_id, async_session)
    print(data)
    order_item = data.order_item
    assert response.status_code == 200
    assert isinstance(order_item, list)
    assert len(order_item) == 1
    assert data.status == 'in_process'
    assert order_item[0].product.name == test_product.name
    assert (
        order_item[0].product.description == test_product.description
    )
    assert float(order_item[0].product.cost) == float(
        test_product.cost
    )


@pytest.mark.anyio
async def test_quantity(async_client, test_product, async_session):
    """Тест: Уменьшение количества товара при создании заказа"""
    test_product_q = test_product.quantity
    item_quantity = 3
    order_data = {
        'order_item': [{"product_id": test_product.id, "item_quantity": item_quantity}]
    }
    response = await async_client.post('/orders/', json=order_data)
    print(response.json())
    data = response.json()
    assert response.status_code == 200 
    assert data.get('order_item')[0]['product'].get('quantity') == test_product_q - item_quantity


@pytest.mark.anyio
async def test_quantity_conflict(async_client, test_product):
    """Тест: Недостаточно товара"""
    order_data = {
        'order_item': [{"product_id": test_product.id, "item_quantity": 10}]
    }

    response = await async_client.post('/orders/', json=order_data)
    assert response.status_code == 409


@pytest.mark.anyio
async def test_status_update(async_client, test_order):
    status_new = {
        "status": "dispatched",
    }
    response = await async_client.patch(
        f'/orders/{test_order.id}/status', json=status_new
    )
    assert response.json()['status'] == 'dispatched'
