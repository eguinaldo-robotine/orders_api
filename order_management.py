import db
from order import Order
from product import Product
from prod_queue import Queue

from flask import Flask, request, jsonify
from flask_cors import CORS

queue = Queue()

for order in db.get_pending():
    queue.put(order)

app = Flask(__name__)
CORS(app)


@app.route('/order/put', methods=['POST'])
def put_order():
    data = request.get_json(silent=True)
    if data:
        try:
            new_order = Order().model_validate(data)
            queue.put(new_order)
            db.insert(new_order)
            return jsonify({
                "status": "success",
                "message": "Order received",
                "order": new_order.model_dump()
            }), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid order format"}), 400


@app.route('/order/get', methods=['GET'])
def get_order():
    current_order = queue.get()
    if current_order:
        current_order.status = "production"
        db.update(current_order)
        return jsonify({
            "status": "success",
            "order": current_order.model_dump()
        }), 200
    return jsonify({"status": "error", "message": "Queue is empty"}), 404


@app.route('/order/finish', methods=['POST'])
def finish_order():
    data = request.get_json(silent=True)
    if data:
        try:
            finished_order = Order().model_validate(data)
            finished_order.status = "completed"
            db.update(finished_order)
            return jsonify({"status": "success", "message": "Order marked as completed"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid order format"}), 400


@app.route('/order/cancel', methods=['POST'])
def cancel_order():
    data = request.get_json(silent=True)
    if data:
        try:
            cancelled_order = Order().model_validate(data)
            if queue.remove(cancelled_order):
                cancelled_order.status = "cancelled"
                db.update(cancelled_order)
                return jsonify({"status": "success", "message": "Order cancelled"}), 200
            else:
                return jsonify({"status": "error", "message": "Order not found in queue"}), 404
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    return jsonify({"status": "error", "message": "Invalid order format"}), 400


@app.route('/order/cancel_by_id', methods=['GET'])
def cancel_order_by_id():
    id = request.args.get('id', default=-1, type=int)
    if id < 0:
        return jsonify({"status": "error", "message": "Invalid ID"}), 400
    cancelled_order = queue.access(id)
    if cancelled_order:
        queue.remove(cancelled_order)
        cancelled_order.status = "cancelled"
        db.update(cancelled_order)
        return jsonify({"status": "success", "message": f"Order {id} cancelled"}), 200
    else:
        return jsonify({"status": "error", "message": "Order not found in queue"}), 404


@app.route('/order/status', methods=['GET'])
def order_status():
    id = request.args.get('id', default=-1, type=int)
    if id < 0:
        return jsonify({"status": "error", "message": "Invalid ID"}), 400
    order = db.get_order(id)
    if order:
        return jsonify({"status": "success", "order_status": order.status}), 200
    else:
        return jsonify({"status": "error", "message": "Order not found"}), 404


@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


if __name__ == '__main__':
    print("   ___          _           ____        _   ")
    print("  / _ \\ _ __ __| | ___ _ __| __ )  ___ | |_ ")
    print(" | | | | '__/ _` |/ _ \\ '__|  _ \\ / _ \\| __|")
    print(" | |_| | | | (_| |  __/ |_ | |_) | (_) | |_ ")
    print("  \\___/|_|  \\__,_|\\___|_(_)|____/ \\___/ \\__|")
    print()
                                                
    app.run(host="0.0.0.0", port=1607, debug=True)