import sqlite3
from typing import List, Optional
from domain.models import Order, Product


class Database:
    
    DATABASE_NAME = 'order_log.db'
    
    def __init__(self):
        self._ensure_table_exists()
    
    def _get_connection(self):
        conn = sqlite3.connect(self.DATABASE_NAME)
        return conn
    
    def _ensure_table_exists(self):
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
    
    def insert(self, order: Order) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        products_json = self._serialize_products(order.products)
        cursor.execute(
            'INSERT INTO Orders (id, box, status, size, products, is_synced) VALUES (?, ?, ?, ?, ?, 0)',
            (order.id, order.box, order.status, order.size, products_json)
        )
        conn.commit()
        conn.close()
    
    def update(self, order: Order) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        products_json = self._serialize_products(order.products)
        cursor.execute('''
            UPDATE Orders
            SET box = ?, status = ?, size = ?, products = ?, is_synced = 0
            WHERE id = ?
        ''', (order.box, order.status, order.size, products_json, order.id))
        conn.commit()
        conn.close()
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
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
                return self._row_to_order(row)
            return None
        except sqlite3.Error as e:
            print(f"[Database] Error getting order {order_id}: {e}")
            return None
        finally:
            conn.close()
    
    def get_pending(self) -> List[Order]:
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
            return orders
        except sqlite3.Error as e:
            print(f"[Database] Error getting pending orders: {e}")
            return []
        finally:
            conn.close()
    
    def _row_to_order(self, row) -> Optional[Order]:
        try:
            import json
            from domain.models import Product, Order
            
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
            print(f"[Database] Error converting row to order: {e}")
            return None
    
    def _serialize_products(self, products: List[Product]) -> str:
        import json
        return json.dumps([product.model_dump() for product in products])

