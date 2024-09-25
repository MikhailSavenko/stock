import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_async_session
from models import Product


async def seed_database(db: AsyncSession):
    """Наполняем БД дефолтными значениями"""
    # Чистим базу
    print('туту')
    await db.execute(Product.__table__.delete())
    
    product_data = [
        {
            "name": "Product A",
            "description": 'Прекрасный продукт А',
            "cost": 100.50,
            "quantity": 10
        },
        {
            "name": "Product B",
            "description": 'Прекрасный продукт B',
            "cost": 1222.50,
            "quantity": 10
        },
        {
            "name": "Product C",
            "description": 'Прекрасный продукт C',
            "cost": 10022.50,
            "quantity": 10
        },
    ]

    for product in product_data:
        new_product = Product(**product)
        db.add(new_product)
    
    await db.commit()  # Не забывайте использовать await


async def main():
    async with get_async_session() as session:  # Получаем асинхронную сессию
        await seed_database(session)  # Передаём сессию в функцию


if __name__ == '__main__':
    asyncio.run(main())  # Запускаем асинхронный main
