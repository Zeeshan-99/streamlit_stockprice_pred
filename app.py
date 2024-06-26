import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import plotly.graph_objects as go

def get_live_stock_price(ticker):
    url = f"https://www.google.com/finance/quote/{ticker}:NSE"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    class1 = "YMlKec fxKbKc"
    price = float(soup.find(class_=class1).text.strip()[1:].replace(",", ""))
    return price

# Streamlit app
st.title('Live Stock Price and Trends App')

ticker = st.text_input('Enter Stock Ticker (e.g., INFY):', 'INFY')

# Display live stock price
price_placeholder = st.empty()

# Initialize empty lists for storing historical stock prices
timestamps = []
prices = []

# Create initial plot
fig = go.Figure()
scatter = fig.add_trace(go.Scatter(x=timestamps, y=prices, mode='lines+markers', name='Stock Price'))
fig.update_layout(title='Live Stock Price Trends',
                  xaxis_title='Timestamp',
                  yaxis_title='Stock Price',
                  template='plotly_dark')

# Display the plot
plot_placeholder = st.plotly_chart(fig)

# Initialize DataFrame
df = pd.DataFrame(columns=['Time', 'Values'])

# Update live stock price and plot every 10 seconds
while True:
    current_price = get_live_stock_price(ticker)
    price_placeholder.text(f'Current Price: {current_price}')

    # Update historical prices lists
    timestamp = pd.Timestamp.now()
    timestamps.append(timestamp)
    prices.append(current_price)

    # Update the plot data
    fig.update_traces(x=timestamps, y=prices)

    # Concatenate new data to the existing DataFrame
    new_df = pd.DataFrame({'Time': [timestamp], 'Values': [current_price]})
    df = pd.concat([df, new_df], ignore_index=True)

    # Redraw the plot
    plot_placeholder.plotly_chart(fig)

    # Wait for 10 seconds before the next update
    time.sleep(10)

    # Clear previous display and show only the concatenated DataFrame
    st.write('Historical Data:', df)
