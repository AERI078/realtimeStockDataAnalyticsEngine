import yfinance as yf
import pandas as pd
from datetime import datetime
import random

"""get ticker data from start_date to end_date"""

def get_ticker_data():
    rand_int = random.randint(800, 1801)
    current_time = datetime.now().strftime("%H:%M:%S")
    return {current_time: rand_int}

def get_dataframe(data):
    df= pd.read_csv("MSFT_stock.csv")