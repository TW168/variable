import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

@st.cache_data
def get_stock_data(ticker, start, end):
    """
    Fetch stock data for the given ticker and date range using Yahoo Finance.

    :param ticker: Stock ticker symbol (e.g., 'AAPL')
    :param start: Start date for the data (datetime object)
    :param end: End date for the data (datetime object)
    :return: DataFrame containing the stock data, or None if an error occurs
    """
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            raise ValueError("No data found for the specified ticker and date range")
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None
    return data



def calculate_sma(data, window):
    """
    Calculate the simple moving average for a given price data and window.

    :param data: DataFrame containing stock price data
    :param window: The window size for the SMA calculation
    :return: Series containing the SMA values
    """
    if data is None or data.empty:
        return None
    sma = data['Close'].rolling(window=window).mean()
    return sma

def sma_strategy(data, short_window, long_window):
    """
    Generate trading signals based on simple moving average crossover strategy.

    :param data: DataFrame containing stock price data
    :param short_window: The window size for the short SMA calculation
    :param long_window: The window size for the long SMA calculation
    :return: DataFrame containing stock price data with additional SMA and trading signal columns
    """
    if data is None or data.empty:
        return None

    data['Short_SMA'] = calculate_sma(data, short_window)
    data['Long_SMA'] = calculate_sma(data, long_window)

    if data['Short_SMA'] is None or data['Long_SMA'] is None:
        return None

    data['Signal'] = 0.0
    data.iloc[short_window:, data.columns.get_loc('Signal')] = np.where(data['Short_SMA'][short_window:] > data['Long_SMA'][short_window:], 1.0, 0.0)
    data['Position'] = data['Signal'].diff()
    return data

def plot_chart(data, ticker):
    """
    Create and return a candlestick chart with short and long SMA lines, as well as buy and sell markers based on
    the SMA strategy.

    :param data: DataFrame containing stock price data with SMA and trading signals
    :param ticker: Stock ticker symbol (e.g., 'AAPL')
    :return: Plotly Figure object
    """
    fig = go.Figure()

    # Add candlestick chart
    fig.add_trace(go.Candlestick(x=data.index,
                                  open=data['Open'],
                                  high=data['High'],
                                  low=data['Low'],
                                  close=data['Close'],
                                  name='Price'))

    # Add short and long SMA lines
    fig.add_trace(go.Scatter(x=data.index, y=data['Short_SMA'], name='Short SMA', line=dict(color='blue', width=1)))
    fig.add_trace(go.Scatter(x=data.index, y=data['Long_SMA'], name='Long SMA', line=dict(color='red', width=1)))

    # Add buy and sell markers
    fig.add_trace(go.Scatter(x=data[data['Position'] == 1].index,
                             y=data[data['Position'] == 1]['Long_SMA'],
                             mode='markers',
                             marker=dict(color='green', size=10, symbol='triangle-up'),
                             name='Buy'))

    fig.add_trace(go.Scatter(x=data[data['Position'] == -1].index,
                             y=data[data['Position'] == -1]['Long_SMA'],
                             mode='markers',
                             marker=dict(color='red', size=10, symbol='triangle-down'),
                             name='Sell'))

    # Customize the chart layout
    fig.update_layout(title=f'{ticker} Price with SMA ',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      width=1300, # Custom width
                      height=600, # Custom height
                      xaxis_rangeslider_visible=False)

    # Display the chart
    return fig