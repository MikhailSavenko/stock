from fastapi import APIRouter, Depends
from app.core.db import AsyncSession, get_async_session
from app.crud.order import order_crud
from app.schemas.order import OrderDB



router = APIRouter()

@router.get('/', response_model=list[OrderDB])
async def get_all_orders(session: AsyncSession = Depends(get_async_session)):
    print('NEEEE')
    return await order_crud.get_multi(session=session)