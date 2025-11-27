from flask import request
from services.order_service import OrderService
from utils.responses import OrderResponse, ApiResponse
from utils.logger import get_logger

logger = get_logger(__name__)


class OrderController:
    
    def __init__(self, order_service: OrderService):
        self.order_service = order_service
    
    def put_order(self):
        data = request.get_json(silent=True)
        
        if not data:
            logger.warning("Tentativa de criar pedido com dados inválidos ou vazios")
            return OrderResponse.invalid_order_format()
        
        try:
            logger.debug(f"Criando pedido com dados: box={data.get('box')}, size={data.get('size')}")
            order = self.order_service.create_order(data)
            logger.info(f"Pedido criado com sucesso: ID={order.id}, Box={order.box}, Status={order.status}")
            return OrderResponse.order_created(order)
        except Exception as e:
            logger.error(f"Erro ao criar pedido: {str(e)}", exc_info=True)
            return ApiResponse.error(message=str(e))
    
    def get_order(self):
        logger.debug("Solicitando próximo pedido da fila")
        order = self.order_service.get_next_order()
        
        if order:
            logger.info(f"Pedido recuperado: ID={order.id}, Box={order.box}, Status={order.status}")
            return OrderResponse.order_retrieved(order)
        
        logger.info("Fila de pedidos está vazia")
        return OrderResponse.queue_empty()
    
    def finish_order(self):
        data = request.get_json(silent=True)
        
        if not data:
            logger.warning("Tentativa de finalizar pedido com dados inválidos ou vazios")
            return OrderResponse.invalid_order_format()
        
        order_id = data.get('id', 'desconhecido')
        logger.debug(f"Finalizando pedido: ID={order_id}")
        
        success = self.order_service.finish_order(data)
        
        if success:
            logger.info(f"Pedido finalizado com sucesso: ID={order_id}")
            return OrderResponse.order_finished()
        
        logger.warning(f"Falha ao finalizar pedido: ID={order_id}")
        return OrderResponse.failed_to_finish()
    
    def cancel_order(self):
        data = request.get_json(silent=True)
        
        if not data:
            logger.warning("Tentativa de cancelar pedido com dados inválidos ou vazios")
            return OrderResponse.invalid_order_format()
        
        order_id = data.get('id', 'desconhecido')
        logger.debug(f"Cancelando pedido: ID={order_id}")
        
        success = self.order_service.cancel_order(data)
        
        if success:
            logger.info(f"Pedido cancelado com sucesso: ID={order_id}")
            return OrderResponse.order_cancelled()
        
        logger.warning(f"Pedido não encontrado na fila para cancelamento: ID={order_id}")
        return OrderResponse.order_not_in_queue()
    
    def cancel_order_by_id(self):
        order_id = request.args.get('id', default=-1, type=int)
        
        if order_id < 0:
            logger.warning(f"Tentativa de cancelar pedido com ID inválido: {order_id}")
            return OrderResponse.invalid_order_id()
        
        logger.debug(f"Cancelando pedido por ID: {order_id}")
        success = self.order_service.cancel_order_by_id(order_id)
        
        if success:
            logger.info(f"Pedido cancelado com sucesso por ID: {order_id}")
            return OrderResponse.order_cancelled(order_id)
        
        logger.warning(f"Pedido não encontrado para cancelamento: ID={order_id}")
        return OrderResponse.order_not_in_queue()
    
    def get_order_status(self):
        order_id = request.args.get('id', default=-1, type=int)
        
        if order_id < 0:
            logger.warning(f"Tentativa de consultar status com ID inválido: {order_id}")
            return OrderResponse.invalid_order_id()
        
        logger.debug(f"Consultando status do pedido: ID={order_id}")
        status = self.order_service.get_order_status(order_id)
        
        if status:
            logger.debug(f"Status do pedido {order_id}: {status}")
            return OrderResponse.order_status(status)
        
        logger.info(f"Pedido não encontrado: ID={order_id}")
        return OrderResponse.order_not_found()
    
    def get_queue_state(self) -> str:
        """Retorna a representação visual do estado atual da fila"""
        return self.order_service.get_queue_state()

