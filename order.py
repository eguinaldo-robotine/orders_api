import json
from typing import List
from pydantic import BaseModel

from product import Product

class Order(BaseModel):
    id : int = -1
    box : int = -1
    status : str = "pending"
    size : int = 0
    products : List[Product] = []

    def __eq__(self, other):
        if(isinstance(other, Order)):
            if(self.id != -1 and other.id != -1):
                return self.id == other.id
        return False
    
    def serialize_products(self):
        return json.dumps([product.model_dump() for product in self.products])
    
    def dump(self):
        return (self.id, self.box, self.status, self.size, self.serialize_products())
    
    def load(self, data):
        id, box, status, size, products_json = data
        products = [Product(**p) for p in json.loads(products_json)]
        self.id = id
        self.box = box
        self.status = status
        self.size = size
        self.products = products
    
    @classmethod
    def load(cls, data):
        id, box, status, size, products_json = data
        products_list = [Product(**p) for p in json.loads(products_json)]
        return cls(id=id, box=box, status=status, size=size, products=products_list)
    