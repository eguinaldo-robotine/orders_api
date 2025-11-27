import sqlite3
from typing import List, Optional
from models.models import Order, Product
from utils.logger import get_logger

logger = get_logger(__name__)


class Database:
    
    DATABASE_NAME = 'order_log.db'
    
    def __init__(self):
        logger.debug(f"Inicializando Database com arquivo: {self.DATABASE_NAME}")
        self._ensure_table_exists()
        logger.debug("Tabela Orders verificada/criada com sucesso")
    
    def _get_connection(self):
        conn = sqlite3.connect(self.DATABASE_NAME)
        return conn
    
    def _ensure_table_exists(self):
        logger.debug("Verificando existência da tabela Orders")
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER DEFAULT -1,
                box INTEGER NOT NULL,
                status TEXT NOT NULL,
                size INTEGER NOT NULL,
                products TEXT NOT NULL,
                timestamp TEXT DEFAULT (datetime('now', 'localtime')),
                is_synced INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
        logger.debug("Tabela Orders garantida")
    
    def insert(self, order: Order) -> None:
        logger.debug(f"Inserindo pedido no banco: ID={order.id}, Box={order.box}, Status={order.status}")
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            products_json = self._serialize_products(order.products)
            cursor.execute(
                'INSERT INTO Orders (id, box, status, size, products, is_synced) VALUES (?, ?, ?, ?, ?, 0)',
                (order.id, order.box, order.status, order.size, products_json)
            )
            conn.commit()
            conn.close()
            logger.info(f"Pedido inserido no banco com sucesso: ID={order.id}")
        except sqlite3.Error as e:
            logger.error(f"Erro ao inserir pedido {order.id} no banco: {str(e)}", exc_info=True)
            raise
    
    def update(self, order: Order) -> None:
        logger.debug(f"Atualizando pedido no banco: ID={order.id}, Status={order.status}")
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            products_json = self._serialize_products(order.products)
            cursor.execute('''
                UPDATE Orders
                SET box = ?, status = ?, size = ?, products = ?, is_synced = 0
                WHERE id = ?
            ''', (order.box, order.status, order.size, products_json, order.id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            
            if rows_affected > 0:
                logger.debug(f"Pedido atualizado no banco: ID={order.id}, Linhas afetadas={rows_affected}")
            else:
                logger.warning(f"Nenhuma linha afetada ao atualizar pedido: ID={order.id}")
        except sqlite3.Error as e:
            logger.error(f"Erro ao atualizar pedido {order.id} no banco: {str(e)}", exc_info=True)
            raise
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        logger.debug(f"Buscando pedido no banco: ID={order_id}")
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, box, status, size, products 
                FROM Orders 
                WHERE id = ?
            ''', (order_id,))
            
            row = cursor.fetchone()
            if row:
                order = self._row_to_order(row)
                logger.debug(f"Pedido encontrado no banco: ID={order_id}, Status={order.status if order else 'None'}")
                return order
            else:
                logger.debug(f"Pedido não encontrado no banco: ID={order_id}")
                return None
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar pedido {order_id} no banco: {str(e)}", exc_info=True)
            return None
        finally:
            conn.close()
    
    def get_pending(self) -> List[Order]:
        logger.debug("Buscando pedidos pendentes no banco de dados")
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, box, status, size, products 
                FROM Orders 
                WHERE status = 'pending'
            ''')
            
            orders = []
            for row in cursor.fetchall():
                order = self._row_to_order(row)
                if order:
                    orders.append(order)
            
            logger.info(f"Encontrados {len(orders)} pedidos pendentes no banco")
            return orders
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar pedidos pendentes: {str(e)}", exc_info=True)
            return []
        finally:
            conn.close()
    
    def _row_to_order(self, row) -> Optional[Order]:
        try:
            import json
            from models.models import Product, Order
            
            order_id, box, status, size, products_json = row
            products_data = json.loads(products_json)
            products = [Product(**p) for p in products_data]
            
            return Order(
                id=order_id,
                box=box,
                status=status,
                size=size,
                products=products
            )
        except Exception as e:
            logger.error(f"Erro ao converter row para Order: {str(e)}", exc_info=True)
            return None
    
    def _serialize_products(self, products: List[Product]) -> str:
        import json
        return json.dumps([product.model_dump() for product in products])

