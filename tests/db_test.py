from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(url='sqlite+aiosqlite:///./fastapi.db')
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
