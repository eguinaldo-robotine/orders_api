from typing import List

from order import Order

class Queue:
    size : int = 0
    items : List[Order] = []

    def put(self, order : Order):
        self.items.append(order)
        self.size = self.size + 1

    def get(self):
        if(self.size > 0):
            self.size = self.size - 1
            return self.items.pop(0)
        return None
    
    def access(self, id : int):
        for item in self.items:
            if(item.id == id):
                return item
        return None
    
    def remove(self, order : Order):
        try:
            self.items.remove(order)
            self.size = self.size - 1
            return True
        except ValueError as e:
            pass
        return False