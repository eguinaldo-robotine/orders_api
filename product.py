from typing import List
from pydantic import BaseModel

class Syrup(BaseModel):
    name : str = ""
    qtd : int = 0

class Topping(BaseModel):
    name : str = ""
    qtd : int = 0

class Product(BaseModel):
    id : int = -1
    cup : int = -1
    type : str = "ice cream"
    status : str = "pending"
    flavour : str = ""
    syrups : List[Syrup] = []
    toppings : List[Topping] = []

    def __eq__(self, other):
        if(isinstance(other, Product)):
            if(self.id != -1 and other.id != -1):
                return self.id == other.id
        return False