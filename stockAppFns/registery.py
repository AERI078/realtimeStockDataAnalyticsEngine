from stockAppFns import hashtable, circular_buffer, sliding_window, min_max_heap

class SymbolRegistry:
    """
    For each symbol having
      - CircularBuffer (recent prices)
      - SlidingWindow (for rolling stats)
      - MinMaxHeap (to track global min/max)
    """
    
    def __init__(self, buffer_size=100, window_size=50):
        self.symbols = hashtable.HashTable()
        self.buffer_size = buffer_size
        self.window_size = window_size

    def register(self, symbol: str): # Register a new symbol with initialized structures if not already registered
        if not self.symbols.contains(symbol):
            self.symbols.put(symbol, {            # putting symbol-dict inside hashtable
                "buffer": circular_buffer.CircularBuffer(self.buffer_size),
                "stats": sliding_window.SlidingWindow(self.window_size),
                "extremes": min_max_heap.MinMaxHeap()
            })

    def get_symbol_data(self, symbol: str) -> dict: # Retrieve data associated with a symbol
        return self.symbols.get(symbol)

    def exists(self, symbol: str) -> bool: # Check if a symbol is already registered
        return self.symbols.contains(symbol)

    def all_symbols(self) -> list: # List all registered symbols
        return self.symbols.keys()
