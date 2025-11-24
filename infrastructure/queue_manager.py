from typing import Optional, List
from collections import deque
from domain.models import Order


class QueueManager:
    
    def __init__(self):
        self._queue: deque = deque()
        self._orders_by_id: dict[int, Order] = {}
    
    def enqueue(self, order: Order) -> None:
        if not isinstance(order, Order):
            raise ValueError("Apenas objetos Order podem ser adicionados à fila")
        
        if order.id != -1 and order.id in self._orders_by_id:
            return
        
        self._queue.append(order)
        if order.id != -1:
            self._orders_by_id[order.id] = order
    
    def dequeue(self) -> Optional[Order]:
        if len(self._queue) == 0:
            return None
        
        order = self._queue.popleft()
        if order.id != -1 and order.id in self._orders_by_id:
            del self._orders_by_id[order.id]
        
        return order
    
    def remove(self, order: Order) -> bool:
        try:
            self._queue.remove(order)
            if order.id != -1 and order.id in self._orders_by_id:
                del self._orders_by_id[order.id]
            return True
        except ValueError:
            return False
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self._orders_by_id.get(order_id)
    
    def is_empty(self) -> bool:
        return len(self._queue) == 0
    
    def size(self) -> int:
        return len(self._queue)

