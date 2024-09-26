from .exeptions import HttpNotFound
from app.crud.order import order_crud
from app.crud.product import product_crud
from app.core.db import AsyncSession


async def get_order_or_404(order_id: int, session: AsyncSession):
    """Проверяем существование объекта. Возвращаем его при наличии"""
    order = await order_crud.get(obj_id=order_id, session=session)
    if not order:
        raise HttpNotFound(detail='Заказа не существует!')
    return order


async def get_product_or_404(product_id: int, session: AsyncSession):
    """Проверяем существование объекта. Возвращаем его при наличии"""
    product = await product_crud.get(obj_id=product_id, session=session)
    if not product:
        raise HttpNotFound(detail='Товара не существует!')
    return product