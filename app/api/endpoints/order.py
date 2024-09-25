from fastapi import APIRouter, Depends
from app.core.db import AsyncSession, get_async_session
from app.crud.order import order_crud
from app.crud.order_item import order_item_crud
from app.schemas.order import OrderCreate, OrderDB

router = APIRouter()

@router.get('/', response_model=list[OrderDB])
async def get_all_orders(session: AsyncSession = Depends(get_async_session)):
    return await order_crud.get_multi(session=session)


@router.get('/{order_id}', response_model=OrderDB)
async def get_order_by_id(session: AsyncSession = Depends(get_async_session)):
    return await order_crud.get(session=session)


@router.post('/', response_model=OrderDB)
async def create_new_order(order_item: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    order = await order_crud.create(session=session)
    print(order)
    await order_item_crud.create(obj_in=order_item, order_id=order.id, session=session)

    return await order_item_crud.get(order.id)