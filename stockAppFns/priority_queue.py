"""Min-heap based priority queue for processing events"""
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def _parent(self, idx):
        return (idx - 1) // 2
    
    def _left_child(self, idx):
        return 2 * idx + 1
    
    def _right_child(self, idx):
        return 2 * idx + 2
    
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def _heapify_up(self, idx):
        while idx > 0:
            parent = self._parent(idx)
            if self.heap[idx][0] < self.heap[parent][0]:
                self._swap(idx, parent)
                idx = parent
            else:
                break
    
    def _heapify_down(self, idx):
        while True:
            smallest = idx
            left = self._left_child(idx)
            right = self._right_child(idx)
            
            if left < self.size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            
            if right < self.size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            
            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break
    
    def push(self, priority, item): # Add item with priority
        self.heap.append((priority, item))
        self.size += 1
        self._heapify_up(self.size - 1)
    
    def pop(self): # Remove and return highest priority item
        if self.size == 0:
            return None
        
        if self.size == 1:
            self.size = 0
            return self.heap.pop()[1]
        
        # Get the root (highest priority)
        root = self.heap[0][1]
        
        # Move last element to root
        self.heap[0] = self.heap.pop()
        self.size -= 1
        
        # Restore heap property
        self._heapify_down(0)
        
        return root
    
    def peek(self): # Get highest priority item without removing
        return self.heap[0][1] if self.size > 0 else None
    
    def is_empty(self):
        return self.size == 0
    
    def __len__(self):
        return self.size