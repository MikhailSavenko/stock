import logging

from fastapi import APIRouter, Depends

from app.api.exeptions import Conflict, NotFound
from app.api.validators import check_quantity_product, get_order_or_404
from app.core.db import AsyncSession, get_async_session
from app.crud.order import order_crud
from app.crud.order_item import order_item_crud
from app.crud.product import product_crud
from app.schemas.order import OrderCreate, OrderDB, OrderUpdate, OrderUpdateDB

router = APIRouter()


@router.get('/', response_model=list[OrderDB])
async def get_all_orders(session: AsyncSession = Depends(get_async_session)):
    try:
        return await order_crud.get_multi(session=session)
    except Exception as e:
        logging.exception(
            'Ошибка при получении списка заказова', stack_info=True
        )
        raise e


@router.get('/{order_id}', response_model=OrderDB)
async def get_order_by_id(
    order_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        await get_order_or_404(order_id=order_id, session=session)
        return await order_crud.get(obj_id=order_id, session=session)
    except NotFound as e:
        raise e
    except Exception as e:
        logging.exception(
            'Ошибка при получении одного заказа', stack_info=True
        )
        raise e


@router.post('/', response_model=OrderDB)
async def create_new_order(
    order_create: OrderCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создание заказа:
    - Проверяем количество товара
    - Создаем Order
    - Cоздаем OrderItem
    - Обновляем количество товара
    - Получаем и отдаем обновленный Order
    """
    try:
        order = await order_crud.create(session=session)
        order_id = order.id
        for order_item in order_create.order_item:
            product, quantity = await check_quantity_product(
                obj_create_order=order_item, session=session
            )
            await order_item_crud.create(
                obj_in=order_item, order_id=order_id, session=session
            )
            await product_crud.update_quantity(
                obj_db=product, session=session, quantity=quantity
            )
        order = await order_crud.get(obj_id=order_id, session=session)
        return order
    except Conflict as e:
        await order_crud.remove(db_obj=order, session=session)
        raise e
    except NotFound as e:
        await order_crud.remove(db_obj=order, session=session)
        raise e
    except Exception as e:
        logging.exception('Ошибка при cоздании заказа', stack_info=True)
        raise e


@router.patch('/{order_id}/status', response_model=OrderUpdateDB)
async def update_status_order(
    order_id: int,
    obj_in: OrderUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        order_obj_db = await get_order_or_404(
            order_id=order_id, session=session
        )
        order_update = await order_crud.update(
            obj_in=obj_in, db_obj=order_obj_db, session=session
        )
        return order_update
    except NotFound as e:
        raise e
    except Exception as e:
        logging.exception('Ошибка при обновлении заказа', stack_info=True)
        raise e
