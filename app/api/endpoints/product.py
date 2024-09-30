import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.api.exeptions import NotFound
from app.api.validators import get_product_or_404
from app.core.db import AsyncSession, get_async_session
from app.crud.product import product_crud
from app.schemas.product import ProductCreate, ProductDB, ProductUpdate

router = APIRouter()


@router.get('/', response_model=list[ProductDB])
async def get_all_products(session: AsyncSession = Depends(get_async_session)):
    try:
        return await product_crud.get_multi(session=session)
    except Exception as e:
        logging.exception(
            'Ошибка при получении списка товаров!', stack_info=True
        )
        raise e


@router.get('/{product_id}', response_model=ProductDB)
async def get_product(
    product_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        await get_product_or_404(product_id=product_id, session=session)
        return await product_crud.get(obj_id=product_id, session=session)
    except NotFound as e:
        raise e
    except Exception as e:
        logging.exception('Ошибка при получении товара!', stack_info=True)
        raise e


@router.post('/', response_model=ProductDB)
async def create_new_product(
    product_item: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        product = await product_crud.create(
            obj_in=product_item, session=session
        )
        return product
    except Exception as e:
        logging.exception('Ошибка при создании товара!', stack_info=True)
        raise e


@router.put('/{product_id}', response_model=ProductDB)
async def update_product(
    product_id: int,
    obj_in: ProductUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        product_obj_db = await get_product_or_404(
            product_id=product_id, session=session
        )
        product_update = await product_crud.update(
            obj_in=obj_in, db_obj=product_obj_db, session=session
        )
        return product_update
    except NotFound as e:
        raise e
    except Exception as e:
        logging.exception('Ошибка при создании товара!', stack_info=True)
        raise e


@router.delete('/{product_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_product(
    product_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        product = await get_product_or_404(
            product_id=product_id, session=session
        )
        await product_crud.remove(db_obj=product, session=session)
        return
    except NotFound as e:
        raise e
    except Exception as e:
        logging.exception('Ошибка при удалении товара!', stack_info=True)
        raise e
