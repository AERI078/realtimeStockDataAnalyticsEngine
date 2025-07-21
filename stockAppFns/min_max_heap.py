class MinMaxHeap:
    def __init__(self):
        self.min_heap = []  # For minimum values
        self.max_heap = []  # For maximum values 
        self.size = 0
    
    def _heapify_up_min(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self.min_heap[idx] < self.min_heap[parent]:
                self.min_heap[idx], self.min_heap[parent] = self.min_heap[parent], self.min_heap[idx]
                idx = parent
            else:
                break
    
    def _heapify_down_min(self, idx):
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            
            if left < len(self.min_heap) and self.min_heap[left] < self.min_heap[smallest]:
                smallest = left
            
            if right < len(self.min_heap) and self.min_heap[right] < self.min_heap[smallest]:
                smallest = right
            
            if smallest != idx:
                self.min_heap[idx], self.min_heap[smallest] = self.min_heap[smallest], self.min_heap[idx]
                idx = smallest
            else:
                break
    
    def _heapify_up_max(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self.max_heap[idx] > self.max_heap[parent]:
                self.max_heap[idx], self.max_heap[parent] = self.max_heap[parent], self.max_heap[idx]
                idx = parent
            else:
                break
    
    def _heapify_down_max(self, idx):
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            
            if left < len(self.max_heap) and self.max_heap[left] > self.max_heap[largest]:
                largest = left
            
            if right < len(self.max_heap) and self.max_heap[right] > self.max_heap[largest]:
                largest = right
            
            if largest != idx:
                self.max_heap[idx], self.max_heap[largest] = self.max_heap[largest], self.max_heap[idx]
                idx = largest
            else:
                break
    
    def add(self, value): # Add value to both heaps
        self.min_heap.append(value)
        self.max_heap.append(value)
        
        self._heapify_up_min(len(self.min_heap) - 1)
        self._heapify_up_max(len(self.max_heap) - 1)
        
        self.size += 1
    
    def get_min(self): # Get minimum value O(1)
        return self.min_heap[0] if self.min_heap else None
    
    def get_max(self): # Get maximum value O(1)
        return self.max_heap[0] if self.max_heap else None
    
    def remove_min(self): # Remove and return minimum value O(log n)
        if not self.min_heap:
            return None
        
        min_val = self.min_heap[0]
        self.min_heap[0] = self.min_heap[-1]
        self.min_heap.pop()
        
        # Remove from max heap too
        self.max_heap.remove(min_val)
        
        if self.min_heap:
            self._heapify_down_min(0)
        
        self.size -= 1
        return min_val
    
    def remove_max(self): # Remove and return maximum value O(log n)
        if not self.max_heap:
            return None
        
        max_val = self.max_heap[0]
        self.max_heap[0] = self.max_heap[-1]
        self.max_heap.pop()
        
        # Remove from min heap too
        self.min_heap.remove(max_val)
        
        if self.max_heap:
            self._heapify_down_max(0)
        
        self.size -= 1
        return max_val
    
    def __len__(self):
        return self.size