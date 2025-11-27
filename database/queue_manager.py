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
        order = self._orders_by_id.get(order_id)
        return order
    
    def is_empty(self) -> bool:
        return len(self._queue) == 0
    
    def size(self) -> int:
        return len(self._queue)
    
    def get_all_orders(self) -> List[Order]:
        """Retorna uma lista com todos os pedidos na fila na ordem atual"""
        return list(self._queue)
    
    def get_queue_state(self) -> str:
        """
        Retorna uma representação visual do estado atual da fila.
        Mostra posição, ID, Box e Status de cada pedido.
        """
        if len(self._queue) == 0:
            return "\n" + "="*60 + "\n  FILA VAZIA - Nenhum pedido aguardando\n" + "="*60 + "\n"
        
        lines = []
        lines.append("\n" + "="*60)
        lines.append(f"  ESTADO DA FILA - Total: {len(self._queue)} pedido(s)")
        lines.append("="*60)
        lines.append(f"{'Pos.':<6} {'ID':<8} {'Box':<6} {'Status':<12} {'Produtos':<10}")
        lines.append("-"*60)
        
        for position, order in enumerate(self._queue, start=1):
            order_id = order.id if order.id != -1 else "N/A"
            box = order.box if order.box != -1 else "N/A"
            status = order.status
            products_count = len(order.products)
            
            lines.append(f"{position:<6} {order_id:<8} {box:<6} {status:<12} {products_count:<10}")
        
        lines.append("="*60 + "\n")
        
        return "\n".join(lines)

