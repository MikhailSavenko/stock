from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Менеджер Складских Операций'
    description: str = 'Сервис для управления процессами на складе.'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()