class CircularBuffer:
    def __init__(self, capacity: int):  
        self.capacity = capacity
        self.size = 0  
        self.head = 0
        self.tail = 0
        self.buffer = [None] * self.capacity 
        self.is_full = False

    def append(self, data)->None: # data appended is a tuple (price, timestamp)
        self.buffer[self.head] = data # add data at newest index
        if self.is_full:
            self.tail = (self.tail + 1) % self.capacity

        self.head = (self.head + 1) % self.capacity 

        self.is_full = (self.head == self.tail)
        self.size = min(self.size + 1, self.capacity) # if size less than capacity then add 1 to size

    
    def remove_oldest(self)->dict:
        if self.size == 0:
            return None
        
        oldest = self.buffer[self.tail]
        self.buffer[self.tail] = None

        self.tail = (self.tail + 1) % self.capacity

        self.size -= 1
        self.is_full = False
        return oldest 


    def return_n_newest(self, n:int=1)->list:
        if n > self.size:
            n = self.size
        
        result = []
        for i in range(n):
            idx = (self.head - 1 - i) % self.capacity
            if self.buffer[idx] is not None:
                result.append(self.buffer[idx])
        
        return result
    

    def get_all(self)->list:
        """Get all items in order (oldest to newest)"""
        if self.size == 0:
            return []
        
        result = []
        for i in range(self.size):
            idx = (self.tail + i) % self.capacity
            result.append(self.buffer[idx])
        
        return result  

    def __len__(self):
        return self.size
    
    def __str__(self):
        return f"CircularBuffer(size={self.size}, capacity={self.capacity})"

        
