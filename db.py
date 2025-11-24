import sqlite3
from typing import List

from order import Order
from product import Product

DATABASE = 'order_log.db'


def insert(order : Order):
    conn = sqlite3.connect(DATABASE)
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
    
    cursor.execute('INSERT INTO Orders (id, box, status, size, products, is_synced) VALUES (?, ?, ?, ?, ?, 0)', order.dump())
    conn.commit()


def update(order : Order):
    conn = sqlite3.connect(DATABASE)
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

    cursor.execute('''
                        UPDATE Orders
                        SET box = ?, status = ?, size = ?, products = ?, is_synced = ?
                        WHERE id = ?
                   ''', 
                   (order.box, order.status, order.size, order.serialize_products(), 0, order.id))
    conn.commit()


def get_order(id : int):
    conn = sqlite3.connect(DATABASE)
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
    
    try:
        cursor.execute(f"""
                            SELECT id, box, status, size, products 
                            FROM Orders 
                            WHERE id = {id}
                        """)
        
        orders : List[Order] = []
        for row in cursor.fetchall():
            order_data = (
                            row[0],
                            row[1],
                            row[2],
                            row[3],
                            row[4]
                          )
            
            order = Order.load(order_data)
            orders.append(order)
            
        if(len(orders) > 1):
            print(f"[dB] Read Order (id = {id}): More than one entry found! Returning first occurrence.")

        if(orders):
            return orders[0]
        else:
            return None
        
    except sqlite3.Error as e:
        print(f"[dB] Read Order (id = {id}): Error --> {e}")
        return None


def get_pending():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    conn.row_factory = sqlite3.Row

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
    
    try:
        cursor.execute("""
                            SELECT id, box, status, size, products 
                            FROM Orders 
                            WHERE status = 'pending'
                       """)
        
        pending_orders = []
        for row in cursor.fetchall():
            order_data = (
                            row[0],
                            row[1],
                            row[2],
                            row[3],
                            row[4]
                          )
            
            order = Order.load(order_data)
            pending_orders.append(order)
            
        return pending_orders
        
    except sqlite3.Error as e:
        print(f"[dB] Retrieve Pending Orders: Error --> {e}")
        return []