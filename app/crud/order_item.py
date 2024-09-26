from .base import CRUDBase
from app.models import OrderItem
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDOrderItem(CRUDBase):
    async def create(self, obj_in, session: AsyncSession, order_id):
        obj_in_data = obj_in.model_dump()
        obj_data = obj_in_data.get('order_item')[0]
        print(f'dfddd {obj_data}')
        db_obj = self.model(**obj_data, order_id=order_id)
        print(f'db_obj {db_obj.__dict__}')
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    
order_item_crud = CRUDOrderItem(OrderItem)