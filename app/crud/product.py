from .base import CRUDBase
from app.models import Product
from app.core.db import AsyncSession


class CRUDProduct(CRUDBase):
    async def update_quantity(self, obj_db: Product, session: AsyncSession, quantity):
        """Обновляем количество товара при заказе"""
        obj_db.quantity = obj_db.quantity - quantity
        session.add(obj_db)
        await session.commit()
        await session.refresh(obj_db)
        return obj_db
        

product_crud = CRUDProduct(Product)