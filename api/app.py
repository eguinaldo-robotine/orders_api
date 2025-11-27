import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from flask import Flask
from flask_cors import CORS

from database.database import Database
from database.queue_manager import QueueManager
from services.order_service import OrderService
from api.http.order_controller import OrderController
from api.http.routes import register_routes
from utils.logger import get_logger

logger = get_logger(__name__)

def create_app():
    logger.info("Inicializando aplicação Flask")
    app = Flask(__name__)
    CORS(app)
    
    logger.debug("Criando instâncias de dependências")
    database = Database()
    queue = QueueManager()
    order_service = OrderService(database, queue)
    order_controller = OrderController(order_service)
    
    logger.info("Carregando pedidos pendentes do banco de dados")
    _load_pending_orders(database, queue)
    
    # Exibe estado inicial da fila
    if queue.size() > 0:
        print(queue.get_queue_state())
    
    logger.info("Registrando rotas da API")
    register_routes(app, order_controller)
    
    logger.info("Aplicação inicializada com sucesso")
    return app


def _load_pending_orders(database: Database, queue: QueueManager):
    pending_orders = database.get_pending()
    logger.info(f"Carregando {len(pending_orders)} pedidos pendentes para a fila")
    
    for order in pending_orders:
        queue.enqueue(order)
        logger.debug(f"Pedido {order.id} adicionado à fila")
    
    logger.info(f"Total de {queue.size()} pedidos na fila após carregamento")


if __name__ == '__main__':
    print("   ___          _           ____        _   ")
    print("  / _ \\ _ __ __| | ___ _ __| __ )  ___ | |_ ")
    print(" | | | | '__/ _` |/ _ \\ '__|  _ \\ / _ \\| __|")
    print(" | |_| | | | (_| |  __/ |_ | |_) | (_) | |_ ")
    print("  \\___/|_|  \\__,_|\\___|_(_)|____/ \\___/ \\__|")
    print()
    
    logger.info("Iniciando servidor Flask")
    app = create_app()
    logger.info("Servidor iniciando em 0.0.0.0:1607 (modo debug)")
    app.run(host="0.0.0.0", port=1607, debug=True)

