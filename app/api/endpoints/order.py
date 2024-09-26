from fastapi import APIRouter, Depends
from app.core.db import AsyncSession, get_async_session
from app.crud.order import order_crud
from app.crud.order_item import order_item_crud
from app.models import Order
from app.schemas.order import OrderCreate, OrderDB
from sqlalchemy.orm import selectinload
from sqlalchemy import select

router = APIRouter()


@router.get('/', response_model=list[OrderDB])
async def get_all_orders(session: AsyncSession = Depends(get_async_session)):
    return await order_crud.get_multi(session=session)


@router.get('/{order_id}', response_model=OrderDB)
async def get_order_by_id(order_id: int, session: AsyncSession = Depends(get_async_session)):
    return await order_crud.get(obj_id=order_id, session=session)


@router.post('/', response_model=OrderDB)
async def create_new_order(order_item: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Создание заказа:
    Создаем Order
    Затем создаем OrderItem 
    Получаем и отдаем  обновленный Order
    """
    order = await order_crud.create(session=session)
    order_id = order.id
    await order_item_crud.create(obj_in=order_item, order_id=order_id, session=session)
    order = await order_crud.get(obj_id=order_id, session=session)
    return order
