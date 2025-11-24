import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from flask import Flask
from flask_cors import CORS
from api.responses import ApiResponse

from infrastructure.database import Database
from infrastructure.queue_manager import QueueManager
from services.order_service import OrderService
from api.controllers.order_controller import OrderController

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    database = Database()
    queue = QueueManager()
    order_service = OrderService(database, queue)
    order_controller = OrderController(order_service)
    
    _load_pending_orders(database, queue)
    _register_routes(app, order_controller)
    
    return app


def _load_pending_orders(database: Database, queue: QueueManager):
    pending_orders = database.get_pending()
    for order in pending_orders:
        queue.enqueue(order)


def _register_routes(app: Flask, controller: OrderController):
    
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


if __name__ == '__main__':
    print("   ___          _           ____        _   ")
    print("  / _ \\ _ __ __| | ___ _ __| __ )  ___ | |_ ")
    print(" | | | | '__/ _` |/ _ \\ '__|  _ \\ / _ \\| __|")
    print(" | |_| | | | (_| |  __/ |_ | |_) | (_) | |_ ")
    print("  \\___/|_|  \\__,_|\\___|_(_)|____/ \\___/ \\__|")
    print()
    
    app = create_app()
    app.run(host="0.0.0.0", port=1607, debug=True)

