from typing import Dict, Any, List


def create_order_data(
    order_id: int = 1,
    box: int = 1,
    status: str = "pending",
    size: int = 1,
    products: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if products is None:
        products = [create_product_data(
            product_id=101,
            cup=2,
            flavour="vanilla",
            syrups=[{"name": "chocolate", "qtd": 1}],
            toppings=[{"name": "peanuts", "qtd": 1}]
        )]
    
    return {
        "id": order_id,
        "box": box,
        "status": status,
        "size": size,
        "products": products
    }


def create_product_data(
    product_id: int = 101,
    cup: int = 2,
    product_type: str = "ice cream",
    status: str = "pending",
    flavour: str = "vanilla",
    syrups: List[Dict[str, Any]] = None,
    toppings: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if syrups is None:
        syrups = []
    if toppings is None:
        toppings = []
    
    return {
        "id": product_id,
        "cup": cup,
        "type": product_type,
        "status": status,
        "flavour": flavour,
        "syrups": syrups,
        "toppings": toppings
    }


def create_order_with_multiple_products(
    order_id: int = 500,
    box: int = 2,
    size: int = 2
) -> Dict[str, Any]:
    products = [
        create_product_data(
            product_id=501,
            cup=2,
            flavour="vanilla",
            syrups=[{"name": "caramel", "qtd": 1}],
            toppings=[{"name": "peanuts", "qtd": 1}]
        ),
        create_product_data(
            product_id=502,
            cup=3,
            flavour="chocolate",
            syrups=[{"name": "chocolate", "qtd": 2}],
            toppings=[{"name": "ovaltine", "qtd": 1}]
        )
    ]
    
    return create_order_data(
        order_id=order_id,
        box=box,
        size=size,
        products=products
    )


def create_simple_order(order_id: int = 100, box: int = 1) -> Dict[str, Any]:
    return create_order_data(
        order_id=order_id,
        box=box,
        products=[create_product_data(
            product_id=200 + order_id,
            flavour="chocolate"
        )]
    )


def create_fake_order(order_id: int = 99999) -> Dict[str, Any]:
    return create_order_data(
        order_id=order_id,
        box=1,
        size=1,
        products=[]
    )


def create_invalid_order() -> Dict[str, Any]:
    return {
        "id": 999,
        "box": 1
    }

