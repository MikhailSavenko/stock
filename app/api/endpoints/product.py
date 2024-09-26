from fastapi import APIRouter, Depends
from app.api.validators import get_product_or_404
from app.core.db import AsyncSession, get_async_session
from app.crud.product import product_crud
from app.schemas.product import ProductCreate, ProductDB

router = APIRouter()


@router.get('/', response_model=list[ProductDB])
async def get_all_products(session: AsyncSession = Depends(get_async_session)):
    return await product_crud.get_multi(session=session)


@router.get('/{product_id}', response_model=ProductDB)
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    await get_product_or_404(product_id=product_id, session=session)
    return await product_crud.get(obj_id=product_id, session=session)


@router.post('/', response_model=ProductDB)
async def create_new_product(product_item: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    product = await product_crud.create(obj_in=product_item, session=session)
    return product


