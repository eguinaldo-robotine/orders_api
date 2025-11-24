from flask import request
from services.order_service import OrderService
from api.http.responses import OrderResponse, ApiResponse


class OrderController:
    
    def __init__(self, order_service: OrderService):
        self.order_service = order_service
    
    def put_order(self):
        data = request.get_json(silent=True)
        
        if not data:
            return OrderResponse.invalid_order_format()
        
        try:
            order = self.order_service.create_order(data)
            return OrderResponse.order_created(order)
        except Exception as e:
            return ApiResponse.error(message=str(e))
    
    def get_order(self):
        order = self.order_service.get_next_order()
        
        if order:
            return OrderResponse.order_retrieved(order)
        
        return OrderResponse.queue_empty()
    
    def finish_order(self):
        data = request.get_json(silent=True)
        
        if not data:
            return OrderResponse.invalid_order_format()
        
        success = self.order_service.finish_order(data)
        
        if success:
            return OrderResponse.order_finished()
        
        return OrderResponse.failed_to_finish()
    
    def cancel_order(self):
        data = request.get_json(silent=True)
        
        if not data:
            return OrderResponse.invalid_order_format()
        
        success = self.order_service.cancel_order(data)
        
        if success:
            return OrderResponse.order_cancelled()
        
        return OrderResponse.order_not_in_queue()
    
    def cancel_order_by_id(self):
        order_id = request.args.get('id', default=-1, type=int)
        
        if order_id < 0:
            return OrderResponse.invalid_order_id()
        
        success = self.order_service.cancel_order_by_id(order_id)
        
        if success:
            return OrderResponse.order_cancelled(order_id)
        
        return OrderResponse.order_not_in_queue()
    
    def get_order_status(self):
        order_id = request.args.get('id', default=-1, type=int)
        
        if order_id < 0:
            return OrderResponse.invalid_order_id()
        
        status = self.order_service.get_order_status(order_id)
        
        if status:
            return OrderResponse.order_status(status)
        
        return OrderResponse.order_not_found()

