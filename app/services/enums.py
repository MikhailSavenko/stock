from enum import Enum


class Status(str, Enum):
    """Статусы заказа"""

    in_process = 'in_process'
    dispatched = 'dispatched'
    delivered = 'delivered'
