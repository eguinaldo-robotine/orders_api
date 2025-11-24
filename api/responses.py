from flask import jsonify
from typing import Any, Optional


class ApiResponse:
    
    @staticmethod
    def success(data: Optional[Any] = None, message: Optional[str] = None, status_code: int = 200):
        response = {"status": "success"}
        
        if message:
            response["message"] = message
        
        if data:
            if isinstance(data, dict):
                response.update(data)
            else:
                response["data"] = data
        
        return jsonify(response), status_code
    
    @staticmethod
    def error(message: str, status_code: int = 400, details: Optional[Any] = None):
        response = {
            "status": "error",
            "message": message
        }
        
        if details:
            response["details"] = details
        
        return jsonify(response), status_code
    
    @staticmethod
    def created(data: Optional[Any] = None, message: Optional[str] = None):
        return ApiResponse.success(data=data, message=message, status_code=201)
    
    @staticmethod
    def not_found(message: str = "Resource not found"):
        return ApiResponse.error(message=message, status_code=404)
    
    @staticmethod
    def bad_request(message: str = "Invalid request"):
        return ApiResponse.error(message=message, status_code=400)
    
    @staticmethod
    def invalid_format(message: str = "Invalid format"):
        return ApiResponse.bad_request(message=message)


class OrderResponse(ApiResponse):
    
    @staticmethod
    def order_created(order: Any):
        return ApiResponse.created(
            data={"order": order.model_dump() if hasattr(order, 'model_dump') else order},
            message="Order received"
        )
    
    @staticmethod
    def order_retrieved(order: Any):
        return ApiResponse.success(
            data={"order": order.model_dump() if hasattr(order, 'model_dump') else order}
        )
    
    @staticmethod
    def order_finished():
        return ApiResponse.success(message="Order marked as completed")
    
    @staticmethod
    def order_cancelled(order_id: Optional[int] = None):
        message = f"Order {order_id} cancelled" if order_id else "Order cancelled"
        return ApiResponse.success(message=message)
    
    @staticmethod
    def order_status(status: str):
        return ApiResponse.success(data={"order_status": status})
    
    @staticmethod
    def queue_empty():
        return ApiResponse.not_found(message="Queue is empty")
    
    @staticmethod
    def order_not_found(message: str = "Order not found"):
        return ApiResponse.not_found(message=message)
    
    @staticmethod
    def invalid_order_format():
        return ApiResponse.invalid_format(message="Invalid order format")
    
    @staticmethod
    def invalid_order_id():
        return ApiResponse.bad_request(message="Invalid ID")
    
    @staticmethod
    def order_not_in_queue():
        return ApiResponse.not_found(message="Order not found in queue")
    
    @staticmethod
    def failed_to_finish():
        return ApiResponse.error(message="Failed to finish order", status_code=400)

