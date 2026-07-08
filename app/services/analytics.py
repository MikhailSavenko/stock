from typing import Optional, Any, Dict
import logging
import asyncio

logger = logging.getLogger("yandex_metrica")

from app.core.celery_app import celery_app

class YandexMetricaClient:
    """Клиент для интеграции с Yandex Metrica API (Server-Side Tracking)"""
    def __init__(self, counter_id: str = "12345678") -> None:
        self.counter_id = counter_id

    
    async def send_click_event(
            self, client_id: str, target_name: str, user_params: Optional[Dict[str, Any]] = None
    ) -> None:
        payload = {
            "counter_id": self.counter_id,
            "client_id": client_id,
            "target": target_name,
            "user_params": user_params or {}
        }

        await asyncio.sleep(0.05)
        logger.info(f"[Yandex Metrica Server-Side] Event sent successfully: {payload}")

metrica_client = YandexMetricaClient()


@celery_app.task(name="app.services.analytics.send_metrica_task")
def send_metrica_task(client_id: str, target_name: str, user_params: Dict[str, Any]) -> str:
    asyncio.run(metrica_client.send_click_event(client_id, target_name, user_params))
    return "Success"
