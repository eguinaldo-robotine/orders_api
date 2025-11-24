from flask import Flask
from api.http.order_controller import OrderController
from api.http.responses import ApiResponse


def register_routes(app: Flask, controller: OrderController):
    """Registra todas as rotas da API de pedidos"""
    
    @app.route('/order/put', methods=['POST'])
    def put_order():
        return controller.put_order()
    
    @app.route('/order/get', methods=['GET'])
    def get_order():
        return controller.get_order()
    
    @app.route('/order/finish', methods=['POST'])
    def finish_order():
        return controller.finish_order()
    
    @app.route('/order/cancel', methods=['POST'])
    def cancel_order():
        return controller.cancel_order()
    
    @app.route('/order/cancel_by_id', methods=['GET'])
    def cancel_order_by_id():
        return controller.cancel_order_by_id()
    
    @app.route('/order/status', methods=['GET'])
    def get_order_status():
        return controller.get_order_status()
    
    @app.errorhandler(404)
    def not_found(e):
        return ApiResponse.not_found(message="Endpoint not found")

