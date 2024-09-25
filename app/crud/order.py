from .base import CRUDBase
from app.models import Order


class CRUDOrder(CRUDBase):
    pass


order_crud = CRUDOrder(Order)