from typing import Optional
from models.models import Order
from database.database import Database
from database.queue_manager import QueueManager


class OrderService:
    
    def __init__(self, database: Database, queue: QueueManager):
        self.database = database
        self.queue = queue
    
    def create_order(self, order_data: dict) -> Order:
        order = Order.model_validate(order_data)
        self.queue.enqueue(order)
        self.database.insert(order)
        return order
    
    def get_next_order(self) -> Optional[Order]:
        order = self.queue.dequeue()
        
        if order:
            order.status = "production"
            self.database.update(order)
        
        return order
    
    def finish_order(self, order_data: dict) -> bool:
        try:
            order = Order.model_validate(order_data)
            order.status = "completed"
            self.database.update(order)
            return True
        except Exception as e:
            print(f"[OrderService] Error finishing order: {e}")
            return False
    
    def cancel_order(self, order_data: dict) -> bool:
        try:
            order = Order.model_validate(order_data)
            self.queue.remove(order)
            order.status = "cancelled"
            self.database.update(order)
            return True
        except Exception as e:
            print(f"[OrderService] Error cancelling order: {e}")
            return False
    
    def cancel_order_by_id(self, order_id: int) -> bool:
        order = self.queue.get_by_id(order_id)
        
        if not order:
            order = self.database.get_by_id(order_id)
        
        if order:
            self.queue.remove(order)
            order.status = "cancelled"
            self.database.update(order)
            return True
        
        return False
    
    def get_order_status(self, order_id: int) -> Optional[str]:
        try:
            order = self.database.get_by_id(order_id)
            return order.status if order else None
        except Exception as e:
            print(f"[OrderService] Error getting order status: {e}")
            return None

