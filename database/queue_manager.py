from typing import Optional, List
from collections import deque
from models.models import Order
from utils.logger import get_logger

logger = get_logger(__name__)


class QueueManager:
    
    def __init__(self):
        logger.debug("Inicializando QueueManager")
        self._queue: deque = deque()
        self._orders_by_id: dict[int, Order] = {}
        logger.debug("QueueManager inicializado")
    
    def enqueue(self, order: Order) -> None:
        if not isinstance(order, Order):
            logger.error("Tentativa de adicionar objeto que não é Order à fila")
            raise ValueError("Apenas objetos Order podem ser adicionados à fila")
        
        if order.id != -1 and order.id in self._orders_by_id:
            logger.debug(f"Pedido {order.id} já está na fila, ignorando adição duplicada")
            return
        
        self._queue.append(order)
        if order.id != -1:
            self._orders_by_id[order.id] = order
        
        logger.debug(f"Pedido adicionado à fila: ID={order.id}, Box={order.box}, Tamanho da fila={len(self._queue)}")
    
    def dequeue(self) -> Optional[Order]:
        if len(self._queue) == 0:
            logger.debug("Tentativa de remover pedido de fila vazia")
            return None
        
        order = self._queue.popleft()
        if order.id != -1 and order.id in self._orders_by_id:
            del self._orders_by_id[order.id]
        
        logger.debug(f"Pedido removido da fila: ID={order.id}, Box={order.box}, Tamanho restante={len(self._queue)}")
        return order
    
    def remove(self, order: Order) -> bool:
        logger.debug(f"Tentando remover pedido da fila: ID={order.id}")
        
        try:
            self._queue.remove(order)
            if order.id != -1 and order.id in self._orders_by_id:
                del self._orders_by_id[order.id]
            logger.debug(f"Pedido removido da fila: ID={order.id}, Tamanho restante={len(self._queue)}")
            return True
        except ValueError:
            logger.debug(f"Pedido não encontrado na fila para remoção: ID={order.id}")
            return False
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self._orders_by_id.get(order_id)
    
    def is_empty(self) -> bool:
        return len(self._queue) == 0
    
    def size(self) -> int:
        return len(self._queue)

