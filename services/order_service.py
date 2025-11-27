from typing import Optional
from models.models import Order
from database.database import Database
from database.queue_manager import QueueManager
from utils.logger import get_logger

logger = get_logger(__name__)


class OrderService:
    
    def __init__(self, database: Database, queue: QueueManager):
        self.database = database
        self.queue = queue
    
    def create_order(self, order_data: dict) -> Order:
        logger.debug(f"Criando pedido a partir dos dados: box={order_data.get('box')}, size={order_data.get('size')}")
        order = Order.model_validate(order_data)
        
        logger.debug(f"Adicionando pedido {order.id} à fila")
        self.queue.enqueue(order)
        
        logger.debug(f"Inserindo pedido {order.id} no banco de dados")
        self.database.insert(order)
        
        logger.info(f"Pedido criado: ID={order.id}, Box={order.box}, Status={order.status}, Produtos={len(order.products)}")
        return order
    
    def get_next_order(self) -> Optional[Order]:
        logger.debug("Buscando próximo pedido da fila")
        queue_size_before = self.queue.size()
        
        order = self.queue.dequeue()
        
        if order:
            logger.info(f"Pedido {order.id} removido da fila e marcado como 'production'")
            order.status = "production"
            self.database.update(order)
            logger.debug(f"Pedidos restantes na fila: {queue_size_before - 1}")
        else:
            logger.debug("Nenhum pedido disponível na fila")
        
        return order
    
    def finish_order(self, order_data: dict) -> bool:
        order_id = order_data.get('id', 'desconhecido')
        logger.debug(f"Finalizando pedido: ID={order_id}")
        
        try:
            order = Order.model_validate(order_data)
            order.status = "completed"
            self.database.update(order)
            logger.info(f"Pedido finalizado com sucesso: ID={order.id}, Box={order.box}")
            return True
        except Exception as e:
            logger.error(f"Erro ao finalizar pedido {order_id}: {str(e)}", exc_info=True)
            return False
    
    def cancel_order(self, order_data: dict) -> bool:
        order_id = order_data.get('id', 'desconhecido')
        logger.debug(f"Cancelando pedido: ID={order_id}")
        
        try:
            order = Order.model_validate(order_data)
            
            removed_from_queue = self.queue.remove(order)
            if removed_from_queue:
                logger.debug(f"Pedido {order.id} removido da fila")
            else:
                logger.debug(f"Pedido {order.id} não estava na fila")
            
            order.status = "cancelled"
            self.database.update(order)
            logger.info(f"Pedido cancelado com sucesso: ID={order.id}, Box={order.box}")
            return True
        except Exception as e:
            logger.error(f"Erro ao cancelar pedido {order_id}: {str(e)}", exc_info=True)
            return False
    
    def cancel_order_by_id(self, order_id: int) -> bool:
        logger.debug(f"Cancelando pedido por ID: {order_id}")
        
        order = self.queue.get_by_id(order_id)
        
        if not order:
            logger.debug(f"Pedido {order_id} não encontrado na fila, buscando no banco de dados")
            order = self.database.get_by_id(order_id)
        
        if order:
            removed_from_queue = self.queue.remove(order)
            if removed_from_queue:
                logger.debug(f"Pedido {order.id} removido da fila")
            
            order.status = "cancelled"
            self.database.update(order)
            logger.info(f"Pedido cancelado com sucesso por ID: {order.id}, Box={order.box}")
            return True
        
        logger.warning(f"Pedido não encontrado para cancelamento: ID={order_id}")
        return False
    
    def get_order_status(self, order_id: int) -> Optional[str]:
        logger.debug(f"Consultando status do pedido: ID={order_id}")
        
        try:
            order = self.database.get_by_id(order_id)
            
            if order:
                logger.debug(f"Status do pedido {order_id}: {order.status}")
                return order.status
            else:
                logger.debug(f"Pedido não encontrado: ID={order_id}")
                return None
        except Exception as e:
            logger.error(f"Erro ao consultar status do pedido {order_id}: {str(e)}", exc_info=True)
            return None
    
    def get_queue_state(self) -> str:
        """Retorna a representação visual do estado atual da fila"""
        return self.queue.get_queue_state()

