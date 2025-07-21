from collections import deque

class SlidingWindow:
    """Efficient sliding window for moving calculations"""
    
    def __init__(self, size: int):
        self.size = size
        self.window = deque(maxlen=size)
        self.sum = 0.0
        self.min_val = float('inf')
        self.max_val = float('-inf')
    
    def add(self, value):
        """Add value to window"""
        if len(self.window) == self.size:
            # Remove oldest value from sum
            old_val = self.window[0]
            self.sum -= old_val
        
        self.window.append(value)
        self.sum += value
        
        # Update min/max efficiently
        self._update_extremes()
    
    def _update_extremes(self):
        """Update min/max values in window"""
        if len(self.window) == 0:
            self.min_val = float('inf')
            self.max_val = float('-inf')
        else:
            self.min_val = min(self.window)
            self.max_val = max(self.window)
    
    def get_average(self):
        """Get moving average O(1)"""
        return self.sum / len(self.window) if self.window else 0
    
    def get_min(self):
        """Get minimum in window"""
        return self.min_val if self.window else None
    
    def get_max(self):
        """Get maximum in window"""
        return self.max_val if self.window else None
    
    def get_range(self):
        """Get price range (max - min)"""
        return self.max_val - self.min_val if self.window else 0
    
    def get_values(self):
        """Get all values in window"""
        return list(self.window)
    
    def is_full(self):
        """Check if window is full"""
        return len(self.window) == self.size
    
    def __len__(self):
        return len(self.window)
