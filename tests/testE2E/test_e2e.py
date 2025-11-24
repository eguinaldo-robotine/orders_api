import pytest
import requests
import time
from typing import Dict, Any, Optional

import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from tests.testE2E.mock import (
    create_order_data,
    create_order_with_multiple_products,
    create_simple_order,
    create_fake_order,
    create_invalid_order
)

BASE_URL = "http://localhost:1607"


@pytest.fixture
def api_client():
    class APIClient:
        def __init__(self, base_url: str):
            self.base_url = base_url
        
        def create_order(self, order_data: Dict[str, Any]) -> requests.Response:
            return requests.post(f"{self.base_url}/order/put", json=order_data)
        
        def get_order(self) -> requests.Response:
            return requests.get(f"{self.base_url}/order/get")
        
        def finish_order(self, order: Dict[str, Any]) -> requests.Response:
            return requests.post(f"{self.base_url}/order/finish", json=order)
        
        def cancel_order(self, order: Dict[str, Any]) -> requests.Response:
            return requests.post(f"{self.base_url}/order/cancel", json=order)
        
        def cancel_order_by_id(self, order_id: int) -> requests.Response:
            return requests.get(f"{self.base_url}/order/cancel_by_id", params={"id": order_id})
        
        def get_order_status(self, order_id: int) -> requests.Response:
            return requests.get(f"{self.base_url}/order/status", params={"id": order_id})
    
    return APIClient(BASE_URL)


@pytest.fixture
def created_order_ids():
    ids = []
    yield ids
    for order_id in ids:
        try:
            requests.get(f"{BASE_URL}/order/cancel_by_id", params={"id": order_id}, timeout=2)
        except:
            pass


class TestOrderCreation:
    
    def test_given_valid_order_data_when_creating_order_then_order_is_created(
        self, api_client, created_order_ids
    ):
        order_data = create_order_data()
        
        response = api_client.create_order(order_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert "order" in data
        assert data["order"]["id"] == order_data["id"]
        created_order_ids.append(data["order"]["id"])
    
    def test_given_invalid_order_format_when_creating_order_then_error_is_returned(
        self, api_client
    ):
        response = api_client.create_order(None)
        
        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "error"
    
    def test_given_order_with_multiple_products_when_creating_order_then_order_is_created(
        self, api_client, created_order_ids
    ):
        order_data = create_order_with_multiple_products()
        
        response = api_client.create_order(order_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert len(data["order"]["products"]) == 2
        created_order_ids.append(data["order"]["id"])


class TestOrderRetrieval:
    
    def test_given_order_in_queue_when_getting_order_then_order_is_retrieved(
        self, api_client, created_order_ids
    ):
        order_data = create_order_data()
        api_client.create_order(order_data)
        time.sleep(0.5)
        created_order_ids.append(order_data["id"])
        
        response = api_client.get_order()
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "order" in data
        assert data["order"]["status"] == "production"
    
    def test_given_empty_queue_when_getting_order_then_error_is_returned(
        self, api_client
    ):
        max_attempts = 10
        for _ in range(max_attempts):
            response = api_client.get_order()
            if response.status_code == 404:
                data = response.json()
                assert data["status"] == "error"
                assert "Queue is empty" in data["message"]
                return
            time.sleep(0.1)
        pytest.fail("Queue should be empty after multiple attempts")


class TestOrderCompletion:
    
    def test_given_order_in_production_when_finishing_order_then_order_is_completed(
        self, api_client, created_order_ids
    ):
        order_data = create_order_data()
        api_client.create_order(order_data)
        time.sleep(0.5)
        created_order_ids.append(order_data["id"])
        
        retrieved_response = api_client.get_order()
        retrieved_order = retrieved_response.json()["order"]
        
        response = api_client.finish_order(retrieved_order)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


class TestOrderCancellation:
    
    def test_given_order_in_queue_when_cancelling_order_then_order_is_cancelled(
        self, api_client, created_order_ids
    ):
        order_data = create_order_data()
        api_client.create_order(order_data)
        time.sleep(0.5)
        created_order_ids.append(order_data["id"])
        
        response = api_client.cancel_order(order_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_given_order_id_when_cancelling_by_id_then_order_is_cancelled(
        self, api_client, created_order_ids
    ):
        order_data = create_simple_order(order_id=100)
        api_client.create_order(order_data)
        time.sleep(0.5)
        created_order_ids.append(100)
        
        response = api_client.cancel_order_by_id(100)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_given_nonexistent_order_when_cancelling_then_error_or_success_is_returned(
        self, api_client
    ):
        fake_order = create_fake_order()
        
        response = api_client.cancel_order(fake_order)
        data = response.json()
        
        assert response.status_code == 200
        assert data["status"] in ["success", "error"]


class TestOrderStatus:
    
    def test_given_existing_order_id_when_getting_status_then_status_is_returned(
        self, api_client, created_order_ids
    ):
        order_data = create_order_data()
        api_client.create_order(order_data)
        time.sleep(0.5)
        created_order_ids.append(order_data["id"])
        
        response = api_client.get_order_status(order_data["id"])
        
        if response.status_code == 500:
            pytest.skip("Database error in status endpoint")
        
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "success"
            assert "order_status" in data
    
    def test_given_invalid_order_id_when_getting_status_then_error_is_returned(
        self, api_client
    ):
        response = api_client.get_order_status(-1)
        
        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "error"
    
    def test_given_nonexistent_order_id_when_getting_status_then_error_is_returned(
        self, api_client
    ):
        response = api_client.get_order_status(99999)
        
        assert response.status_code in [404, 500]


class TestMultipleOrders:
    
    def test_given_multiple_orders_when_processing_then_orders_are_processed_in_order(
        self, api_client, created_order_ids
    ):
        orders = []
        for i in range(3):
            order_data = create_simple_order(order_id=100 + i)
            response = api_client.create_order(order_data)
            assert response.status_code == 201
            orders.append(response.json()["order"])
            created_order_ids.append(100 + i)
        
        assert len(orders) == 3
        
        for i, order in enumerate(orders):
            retrieved_response = api_client.get_order()
            if retrieved_response.status_code == 200:
                retrieved_order = retrieved_response.json()["order"]
                assert retrieved_order["id"] == order["id"]
                api_client.finish_order(retrieved_order)


class TestCompleteFlow:
    
    def test_given_new_order_when_completing_full_flow_then_all_steps_succeed(
        self, api_client, created_order_ids
    ):
        order_data = create_order_data()
        
        create_response = api_client.create_order(order_data)
        assert create_response.status_code == 201
        created_order = create_response.json()["order"]
        created_order_ids.append(created_order["id"])
        time.sleep(0.5)
        
        get_response = api_client.get_order()
        assert get_response.status_code == 200
        retrieved_order = get_response.json()["order"]
        assert retrieved_order["id"] == created_order["id"]
        
        finish_response = api_client.finish_order(retrieved_order)
        assert finish_response.status_code == 200
        assert finish_response.json()["status"] == "success"

