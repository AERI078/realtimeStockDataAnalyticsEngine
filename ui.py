import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random
import sys
import os
from queue import Queue
import threading

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data_engine import RealTimeDataEngine
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Make sure data_engine.py and the stockAppFns folder are in the same directory as this Streamlit app")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Real-Time Stock Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state with proper defaults
def init_session_state():
    if 'engine' not in st.session_state:
        st.session_state.engine = RealTimeDataEngine(buffer_size=100, window_size=20)
    
    if 'symbols' not in st.session_state:
        st.session_state.symbols = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "INFY", "NVDA"]
    
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = False
    
    if 'data_queue' not in st.session_state:
        st.session_state.data_queue = Queue()
    
    if 'base_prices' not in st.session_state:
        st.session_state.base_prices = {symbol: random.uniform(100, 500) for symbol in st.session_state.symbols}

init_session_state()

# Sidebar controls
st.sidebar.title("🎛️ Controls")

# Symbol management
st.sidebar.subheader("Symbol Management")
new_symbol = st.sidebar.text_input("Add New Symbol", placeholder="e.g., META")
if st.sidebar.button("Add Symbol"):
    if new_symbol and new_symbol.upper() not in st.session_state.symbols:
        st.session_state.symbols.append(new_symbol.upper())
        st.session_state.base_prices[new_symbol.upper()] = random.uniform(100, 500)
        st.sidebar.success(f"Added {new_symbol.upper()}")

# Display current symbols
st.sidebar.write("**Current Symbols:**")
for symbol in st.session_state.symbols:
    st.sidebar.write(f"• {symbol}")

# Simulation controls
st.sidebar.subheader("Data Simulation")
simulation_speed = st.sidebar.slider("Speed (updates/sec)", 1, 10, 3)
price_volatility = st.sidebar.slider("Price Volatility", 0.1, 5.0, 1.0)

class DataSimulator:
    def __init__(self, engine, symbols, base_prices):
        self.engine = engine
        self.symbols = symbols.copy()  # Create a copy
        self.base_prices = base_prices.copy()  # Create a copy
        self.running = False
        self.thread = None
    
    def simulate_data(self, speed, volatility):
        """Background simulation function"""
        while self.running:
            try:
                symbol = random.choice(self.symbols)
                # Add some trending behavior
                self.base_prices[symbol] *= random.uniform(0.99, 1.01)
                noise = random.uniform(-volatility, volatility)
                price = max(1, self.base_prices[symbol] + noise)
                
                self.engine.ingest(symbol, round(price, 2))
                time.sleep(1.0 / speed)
            except Exception as e:
                print(f"Simulation error: {e}")
                break
    
    def start(self, speed, volatility):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.simulate_data, args=(speed, volatility), daemon=True)
            self.thread.start()
            return True
        return False
    
    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)

# Initialize simulator if not exists
if 'simulator' not in st.session_state:
    st.session_state.simulator = DataSimulator(
        st.session_state.engine, 
        st.session_state.symbols, 
        st.session_state.base_prices
    )

# Start/Stop simulation
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("▶️ Start", disabled=st.session_state.simulation_running):
        if st.session_state.simulator.start(simulation_speed, price_volatility):
            st.session_state.simulation_running = True
            st.success("Started!")

with col2:
    if st.button("⏹️ Stop", disabled=not st.session_state.simulation_running):
        st.session_state.simulator.stop()
        st.session_state.simulation_running = False
        st.success("Stopped!")

# Manual data adding for testing
st.sidebar.subheader("Manual Testing")
test_symbol = st.sidebar.selectbox("Symbol", st.session_state.symbols)
test_price = st.sidebar.number_input("Price", min_value=1.0, value=250.0, step=1.0)
if st.sidebar.button("Add Data Point"):
    st.session_state.engine.ingest(test_symbol, test_price)
    st.sidebar.success(f"Added {test_symbol} @ ${test_price}")

# Main dashboard
st.title("📈 Real-Time Stock Analytics Engine")
st.markdown("---")

# Create dashboard function
def create_dashboard():
    # Get all current data
    all_data = st.session_state.engine.get_all_data()
    
    if not all_data:
        st.info("🚀 Start the simulation or manually add data points to begin!")
        return
    
    # Key metrics row
    st.subheader("📊 Key Metrics")
    cols = st.columns(4)
    
    active_symbols = len(all_data)
    total_points = st.session_state.engine.total_points
    
    with cols[0]:
        st.metric("Active Symbols", active_symbols)
    
    with cols[1]:
        st.metric("Total Data Points", total_points)
    
    with cols[2]:
        valid_prices = [data['latest'] for data in all_data.values() if data['latest']]
        avg_price = sum(valid_prices) / len(valid_prices) if valid_prices else 0
        st.metric("Avg Current Price", f"${avg_price:.2f}")
    
    with cols[3]:
        processing_rate = st.session_state.engine.total_points / max(st.session_state.engine.total_time, 0.001)
        st.metric("Processing Rate", f"{processing_rate:.1f} pts/sec")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Current Prices vs Rolling Average")
        
        # Prepare data for price comparison
        symbols = []
        current_prices = []
        rolling_avgs = []
        
        for symbol, data in all_data.items():
            if data['latest'] and data['avg']:
                symbols.append(symbol)
                current_prices.append(data['latest'])
                rolling_avgs.append(data['avg'])
        
        if symbols:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Current Price',
                x=symbols,
                y=current_prices,
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                name='Rolling Average',
                x=symbols,
                y=rolling_avgs,
                marker_color='orange'
            ))
            
            fig.update_layout(
                barmode='group',
                height=400,
                yaxis_title="Price ($)",
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for price comparison yet")
    
    with col2:
        st.subheader("📈 Price Ranges (Min-Max)")
        
        # Prepare data for range chart
        range_symbols = []
        min_prices = []
        max_prices = []
        
        for symbol, data in all_data.items():
            if data['min'] and data['max'] and data['min'] != data['max']:
                range_symbols.append(symbol)
                min_prices.append(data['min'])
                max_prices.append(data['max'])
        
        if range_symbols:
            fig = go.Figure()
            
            for i, symbol in enumerate(range_symbols):
                fig.add_trace(go.Scatter(
                    x=[symbol, symbol],
                    y=[min_prices[i], max_prices[i]],
                    mode='lines+markers',
                    name=symbol,
                    line=dict(width=8),
                    marker=dict(size=12)
                ))
            
            fig.update_layout(
                height=400,
                yaxis_title="Price ($)",
                xaxis_title="Symbol",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No range data available yet")
    
    # Recent price movements
    st.subheader("⏰ Recent Price Movements")
    
    # Get recent data for each symbol
    recent_data = {}
    for symbol in st.session_state.symbols:
        if st.session_state.engine.registry.exists(symbol):
            buffer = st.session_state.engine.registry.get_symbol_data(symbol)["buffer"]
            recent = buffer.return_n_newest(20)  # Get last 20 points
            if recent and len(recent) > 1:  # Only show if we have multiple points
                recent_data[symbol] = recent
    
    if recent_data:
        fig = go.Figure()
        
        for symbol, data_points in recent_data.items():
            prices = [point[0] for point in reversed(data_points)]  # Reverse to show chronologically
            x_values = list(range(len(prices)))
            
            fig.add_trace(go.Scatter(
                x=x_values,
                y=prices,
                mode='lines+markers',
                name=symbol,
                line=dict(width=2),
                marker=dict(size=4)
            ))
        
        fig.update_layout(
            height=400,
            title="Recent Price Trends (Last 20 Data Points)",
            xaxis_title="Data Point Index",
            yaxis_title="Price ($)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data points for trend analysis yet")
    
    # Data table
    st.subheader("📋 Symbol Summary Table")
    
    if all_data:
        df_data = []
        for symbol, data in all_data.items():
            df_data.append({
                "Symbol": symbol,
                "Latest Price": f"${data['latest']:.2f}" if data['latest'] else "N/A",
                "Rolling Avg": f"${data['avg']:.2f}" if data['avg'] else "N/A",
                "Min": f"${data['min']:.2f}" if data['min'] else "N/A",
                "Max": f"${data['max']:.2f}" if data['max'] else "N/A",
                "Range": f"${data['max'] - data['min']:.2f}" if data['min'] and data['max'] else "N/A",
                "Trend": "🟢 Above Avg" if (data['latest'] and data['avg'] and data['latest'] > data['avg']) else "🔴 Below Avg"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
    
    # Price alerts section
    st.subheader("🚨 Price Alerts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        threshold_high = st.number_input("High Price Alert ($)", min_value=0.0, value=300.0, step=10.0)
        high_alerts = st.session_state.engine.symbols_above_price(threshold_high)
        
        if high_alerts:
            st.error(f"🔥 {len(high_alerts)} symbols above ${threshold_high}:")
            for symbol, price in high_alerts:
                st.write(f"• **{symbol}**: ${price:.2f}")
        else:
            st.success(f"✅ No symbols above ${threshold_high}")
    
    with col2:
        threshold_low = st.number_input("Low Price Alert ($)", min_value=0.0, value=150.0, step=10.0)
        low_alerts = st.session_state.engine.symbols_below_price(threshold_low)
        
        if low_alerts:
            st.warning(f"⚠️ {len(low_alerts)} symbols below ${threshold_low}:")
            for symbol, price in low_alerts:
                st.write(f"• **{symbol}**: ${price:.2f}")
        else:
            st.success(f"✅ No symbols below ${threshold_low}")

# Create the dashboard
create_dashboard()

# Auto-refresh logic - only refresh if simulation is running
if st.session_state.simulation_running:
    time.sleep(1)
    st.rerun()

# Footer
st.markdown("---")
st.markdown("*Real-Time Stock Analytics Engine*")
st.markdown("*Arushi 2025*")