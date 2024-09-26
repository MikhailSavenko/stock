from app.schemas.order import OrderCreate
from .exeptions import HttpNotFound, Conflict
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


async def check_quantity_product(obj_create_order: OrderCreate, session: AsyncSession):
    """Проверяем достаточное количество товара на складе для заказа"""
    obj_in_data = obj_create_order.model_dump()
    data_order = obj_in_data.get('order_item')[0]
    required_quantity = data_order.get('item_quantity')
    product_id = data_order.get('product_id')
    product = await get_product_or_404(product_id=product_id, session=session)  
    if required_quantity > product.quantity:
        raise Conflict(detail=f'Заказ не может быть обработан: на складе недостаточно товара. Возможное количество для заказа: {product.quantity}.')
    return data_order