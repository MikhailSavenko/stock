from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Менеджер Складских Операций'
    description: str = 'Сервис для управления процессами на складе.'
    database_url: str = 'postgresql+asyncpg://stock:stocksuper@db:5432/stock'
    secret: str = 'SECRET'
    celery_broker_url: str = "redis://redis:6379/0"

    class Config:
        env_file = '.env'
        extra = 'allow'


settings = Settings()
