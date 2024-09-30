import pytest


@pytest.mark.anyio
async def test_get_all_products(async_client):
    """Тест: Получение Списка объектов при GET /products"""
    response = await async_client.get('/products/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_one_product(async_client, test_product):
    """Тест: Получение объекта по id: GET products/id"""
    response = await async_client.get(f'/products/{test_product.id}')
    assert response.status_code == 200
    assert response.json()['id'] == test_product.id
    assert response.json()['name'] == test_product.name
    assert response.json()['description'] == test_product.description
    assert float(response.json()['cost']) == float(test_product.cost)
    assert response.json()['quantity'] == test_product.quantity


@pytest.mark.anyio
async def test_create_products(async_client):
    """Тест: Создание Товара"""
    data = {
        "name": "Product test",
        "description": "test",
        "cost": 1000,
        "quantity": 2
    }
    response = await async_client.post(f'/products/', json=data)
    if response.status_code == 200:
        response_data = response.json()
        assert response_data['name'] == data['name']
        assert response_data['description'] == data['description']
        assert response_data['cost'] == data['cost']
        assert response_data['quantity'] == data['quantity']


@pytest.mark.anyio
async def test_update_product(async_client, test_product):
    """Тест: Изменение объекта PUT product/id"""
    data_in = {
        "name": "update",
        "description": "update",
        "cost": 1000,
        "quantity": 10
    }
    response = await async_client.put(f'/products/{test_product.id}', json=data_in)
    if response.status_code == 200:
        response_data = response.json()
        assert response_data['name'] == data_in['name']
        assert response_data['description'] == data_in['description']
        assert response_data['cost'] == data_in['cost']
        assert response_data['quantity'] == data_in['quantity']

@pytest.mark.anyio
async def test_del_product(async_client, test_product):
    """Тест: Удаление объекта DELETE product/id"""
    response = await async_client.delete(f'/products/{test_product.id}')
    assert response.status_code == 204