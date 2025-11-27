from flask import Flask, request
from api.http.order_controller import OrderController
from utils.responses import ApiResponse
from utils.logger import get_logger

logger = get_logger(__name__)


def _display_queue_state(controller: OrderController):
    """Exibe o estado atual da fila no console"""
    queue_state = controller.get_queue_state()
    print(queue_state)


def register_routes(app: Flask, controller: OrderController):
    """Registra todas as rotas da API de pedidos"""
    
    @app.route('/order/put', methods=['POST'])
    def put_order():
        logger.info(f"POST /order/put - IP: {request.remote_addr}")
        response = controller.put_order()
        logger.debug(f"POST /order/put - Status: {response[1]}")
        return response
    
    @app.route('/order/get', methods=['GET'])
    def get_order():
        logger.info(f"GET /order/get - IP: {request.remote_addr}")
        response = controller.get_order()
        logger.debug(f"GET /order/get - Status: {response[1]}")
        return response
    
    @app.route('/order/finish', methods=['POST'])
    def finish_order():
        logger.info(f"POST /order/finish - IP: {request.remote_addr}")
        response = controller.finish_order()
        logger.debug(f"POST /order/finish - Status: {response[1]}")
        return response
    
    @app.route('/order/cancel', methods=['POST'])
    def cancel_order():
        logger.info(f"POST /order/cancel - IP: {request.remote_addr}")
        response = controller.cancel_order()
        logger.debug(f"POST /order/cancel - Status: {response[1]}")
        return response
    
    @app.route('/order/cancel_by_id', methods=['GET'])
    def cancel_order_by_id():
        order_id = request.args.get('id', default=-1, type=int)
        logger.info(f"GET /order/cancel_by_id?id={order_id} - IP: {request.remote_addr}")
        response = controller.cancel_order_by_id()
        logger.debug(f"GET /order/cancel_by_id - Status: {response[1]}")
        return response
    
    @app.route('/order/status', methods=['GET'])
    def get_order_status():
        order_id = request.args.get('id', default=-1, type=int)
        logger.info(f"GET /order/status?id={order_id} - IP: {request.remote_addr}")
        response = controller.get_order_status()
        logger.debug(f"GET /order/status - Status: {response[1]}")
        return response
    
    @app.route('/queue/status', methods=['GET'])
    def get_queue_status():
        """Exibe o estado atual da fila no console e retorna informações em JSON"""
        logger.info(f"GET /queue/status - IP: {request.remote_addr}")
        _display_queue_state(controller)
        return ApiResponse.success(
            data={"message": "Queue state displayed in console"},
            message="Queue state displayed successfully"
        )
    
    @app.errorhandler(404)
    def not_found(e):
        logger.warning(f"404 - Endpoint não encontrado: {request.path} - IP: {request.remote_addr}")
        return ApiResponse.not_found(message="Endpoint not found")

