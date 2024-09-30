import pytest


@pytest.mark.anyio
async def test_get_all_orders(async_client):
    print(async_client)
    response = await async_client.get('/orders/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_one_order(async_client, test_order):
    response = await async_client.get(f'/orders/{test_order.id}')
    assert response.status_code == 200
    assert response.json()['id'] == test_order.id
    assert response.json()['status']
    assert isinstance(response.json()['order_item'], list)



    
    
