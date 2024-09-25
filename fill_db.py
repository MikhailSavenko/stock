import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import AsyncSessionLocal
from app.models import Product


async def seed_database(db: AsyncSession):
    """Наполняем БД значениями"""
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
    
    await db.commit()  


async def main():
    async with AsyncSessionLocal() as session:
        await seed_database(session) 
        

if __name__ == '__main__':
    asyncio.run(main()) 
