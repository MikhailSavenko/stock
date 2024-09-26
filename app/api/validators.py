from .exeptions import HttpNotFound
from app.crud.order import order_crud
from app.core.db import AsyncSession


async def get_order_or_404(order_id: int, session: AsyncSession):
    """Проверяем существование объекта. Возвращаем его при наличии"""
    order = await order_crud.get(obj_id=order_id, session=session)
    if not order:
        raise HttpNotFound(detail='Заказа не существует!')
    return order