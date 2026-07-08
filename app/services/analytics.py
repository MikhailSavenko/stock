import logging
import asyncio

logger = logging.getLogger("yandex_metrica")

from app.core.celery_app import celery_app

class YandexMetricaClient:
    """Клиент для интеграции с Yandex Measurement Protocol"""
    def __init__(self, tid: str = "Young&Junior") -> None:
        self.tid = tid

    
    async def send_click_event(
            self, client_id: str, order_id: int, price: float) -> None:
        payload = {
            "tid": self.tid,
            "cid": client_id,
            "t": "event",
            "pa": "purchase",
            "ti": str(order_id),
            "tr": price,
            "cu": "RUB"
        }
        await asyncio.sleep(0.05)
        logger.info(f"[Yandex Measurement Protocol] Event sent successfully: {payload}")

metrica_client = YandexMetricaClient()


@celery_app.task(name="app.services.analytics.send_metrica_task")
def send_metrica_task(client_id: str, order_id: int, price: float) -> str:
    asyncio.run(metrica_client.send_click_event(client_id, order_id, price))
    return "Success"
