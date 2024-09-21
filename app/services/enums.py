from sqlalchemy import Enum


class Status(Enum):
    """Статусы заказа"""
    IN_PROCESS = 'in_process'
    DISPATCHED = 'dispatched'
    DELIVERED = 'delivered'