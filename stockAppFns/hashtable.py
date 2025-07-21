# using for stock symbol lookups
class HashTable:
    def __init__(self, initial_capacity: int = 16):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        self.load_factor_threshold = 0.75
    
    def _hash(self, key: str) -> int: # hash function
        hash_val = 0
        for char in key:
            hash_val = (hash_val * 31 + ord(char)) % self.capacity
        return hash_val
    
    def _resize(self): # Resize hash table when load factor exceeded
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        
        # Rehash all items
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def put(self, key: str, value): # Insert or update key-value pair
        if self.size >= self.capacity * self.load_factor_threshold:
            self._resize()
        
        hash_val = self._hash(key)
        bucket = self.buckets[hash_val]
        
        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Add new key-value pair
        bucket.append((key, value))
        self.size += 1
    
    def get(self, key: str):
        """Get value by key"""
        hash_val = self._hash(key)
        bucket = self.buckets[hash_val]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return None
    
    def remove(self, key: str):
        """Remove key-value pair"""
        hash_val = self._hash(key)
        bucket = self.buckets[hash_val]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return v
        
        return None
    
    def contains(self, key: str) -> bool: # Check if key exists
        return self.get(key) is not None
    
    def keys(self): # Get all keys
        keys = []
        for bucket in self.buckets:
            for k, v in bucket:
                keys.append(k)
        return keys
    
    def values(self): # Get all values
        values = []
        for bucket in self.buckets:
            for k, v in bucket:
                values.append(v)
        return values
    
    def __len__(self):
        return self.size