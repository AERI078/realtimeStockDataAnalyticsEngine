import time
from typing import List, Dict
from dataclasses import dataclass
from stockAppFns import registery, priority_queue

@dataclass
class StockData:
    symbol: str
    price: float
    volume: int
    timestamp: float  #unix

class RealTimeDataEngine: # using SymbolRegistry to manage per-symbol structures.

    def __init__(self, buffer_size=100, window_size=50):
        self.registry = registery.SymbolRegistry(buffer_size, window_size)
        self.total_points = 0
        self.total_time = 0.0

    def process_point(self, data: StockData):
        """Process a single StockData point"""
        symbol = data.symbol
        self.registry.register(symbol)

        symbol_data = self.registry.get_symbol_data(symbol)

        # Update data structures
        symbol_data["buffer"].append((data.price, data.timestamp))
        symbol_data["stats"].add(data.price)
        symbol_data["extremes"].add(data.price)

    # def process_batch(self, data_list: List[StockData]) -> Dict[str, float]:
    #     """Process a batch of StockData points"""
    #     start_time = time.perf_counter()

    #     for data in data_list:
    #         self.process_point(data)

    #     end_time = time.perf_counter()
    #     batch_time = end_time - start_time

    #     self.total_points += len(data_list)
    #     self.total_time += batch_time

    #     return {
    #         "batch_size": len(data_list),
    #         "batch_time": batch_time,
    #         "total_points": self.total_points,
    #         "total_time": self.total_time,
    #         "points_per_second": self.total_points / self.total_time if self.total_time else 0
    #     }
    
    def ingest(self, symbol: str, price: float):
        """Convenience method for simulator"""
        data = StockData(symbol, price, 0, time.time())
        self.process_point(data)

    def get_latest_price(self, symbol: str):
        if not self.registry.exists(symbol):
            return None
        buffer = self.registry.get_symbol_data(symbol)["buffer"]
        recent = buffer.return_n_newest(1)
        return recent[0][0] if recent else None

    def get_rolling_average(self, symbol: str) -> float:
        """Get current rolling average"""
        if not self.registry.exists(symbol):
            return None
        return self.registry.get_symbol_data(symbol)["stats"].get_average()

    def get_min_max(self, symbol: str):
        """Get current min and max prices"""
        if not self.registry.exists(symbol):
            return (None, None)
        extremes = self.registry.get_symbol_data(symbol)["extremes"]
        return (extremes.get_min(), extremes.get_max())

    def list_symbols(self) -> List[str]:
        """Return all currently registered symbols"""
        return self.registry.all_symbols()

    def symbols_above_price(self, threshold: float):
        """Return all symbols where latest price is above threshold"""
        result = []
        for symbol in self.list_symbols():
            price = self.get_latest_price(symbol)
            if price is not None and price > threshold:
                result.append((symbol, price))
        return result

    def symbols_below_price(self, threshold: float):
        """Return all symbols where latest price is below threshold"""
        result = []
        for symbol in self.list_symbols():
            price = self.get_latest_price(symbol)
            if price is not None and price < threshold:
                result.append((symbol, price))
        return result

    def symbols_above_average(self):
        """Return all symbols where latest price > rolling average"""
        result = []
        for symbol in self.list_symbols():
            price = self.get_latest_price(symbol)
            avg = self.get_rolling_average(symbol)
            if price is not None and avg is not None and price > avg:
                result.append((symbol, price, avg))
        return result

    def get_all_data(self) -> dict:
        """Get complete snapshot of all symbol data"""
        snapshot = {}
        for symbol in self.list_symbols():
            snapshot[symbol] = {
                "latest": self.get_latest_price(symbol),
                "avg": self.get_rolling_average(symbol),
                "min": self.get_min_max(symbol)[0],
                "max": self.get_min_max(symbol)[1]
            }
        return snapshot


class EventProcessor:
    def __init__(self):
        self.queue = priority_queue.PriorityQueue()  # custom priority queue

    def add_event(self, priority: int, action: str):
        self.queue.push(priority, action)

    def process_next(self):
        if not self.queue.is_empty():
            event = self.queue.pop() 
            print(f"[ALERT] {event}")
            return event
        return None

    def process_all(self):
        while not self.queue.is_empty():
            self.process_next()
