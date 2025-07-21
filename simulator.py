import random
import time
from data_engine import RealTimeDataEngine

def simulate_feed(engine, symbols: list[str], steps=100, delay=0.1):
    for _ in range(steps):
        symbol = random.choice(symbols)
        price = round(random.uniform(100, 500), 2)
        print(f"Ingesting: {symbol} @ {price}")
        engine.ingest(symbol, price)
        time.sleep(delay)

if __name__=="__main__":
    engine = RealTimeDataEngine(buffer_size=100, window_size=5)
    symbols = ["AAPL", "TSLA", "INFY"]

    simulate_feed(engine, symbols, steps=50, delay=0.2)