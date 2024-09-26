from fastapi import APIRouter, Depends
from app.api.validators import check_quantity_product, get_order_or_404
from app.core.db import AsyncSession, get_async_session
from app.crud.order import order_crud
from app.crud.order_item import order_item_crud
from app.schemas.order import OrderCreate, OrderDB, OrderUpdate, OrderUpdateDB

router = APIRouter()


@router.get('/', response_model=list[OrderDB])
async def get_all_orders(session: AsyncSession = Depends(get_async_session)):
    return await order_crud.get_multi(session=session)


@router.get('/{order_id}', response_model=OrderDB)
async def get_order_by_id(order_id: int, session: AsyncSession = Depends(get_async_session)):
    await get_order_or_404(order_id=order_id, session=session)
    return await order_crud.get(obj_id=order_id, session=session)


@router.post('/', response_model=OrderDB)
async def create_new_order(order_item: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Создание заказа:
    - Проверяем количество товара
    - Создаем Order
    - Затем создаем OrderItem 
    - Получаем и отдаем обновленный Order
    """
    await check_quantity_product(obj_create_order=order_item, session=session)
    order = await order_crud.create(session=session)
    order_id = order.id
    await order_item_crud.create(obj_in=order_item, order_id=order_id, session=session)
    order = await order_crud.get(obj_id=order_id, session=session)
    return order


@router.patch('/{order_id}/status', response_model=OrderUpdateDB)
async def update_status_order(order_id: int, obj_in: OrderUpdate, session: AsyncSession = Depends(get_async_session)):
    order_obj_db = await get_order_or_404(order_id=order_id, session=session)
    order_update = await order_crud.update(obj_in=obj_in, db_obj=order_obj_db, session=session)
    return order_update