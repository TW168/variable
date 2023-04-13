# import pandas as pd
# import numpy as np
# import yfinance as yf
from datetime import datetime, timedelta
# import plotly.express as px
# import plotly.graph_objects as go
import streamlit as st
from sma import get_stock_data, sma_strategy, plot_chart

# Set page configuration
st.set_page_config(page_title='Strategies', layout='wide')

# Display title
st.title("Strategies")

# Input fields for user to enter data
# ticker = st.sidebar.text_input("Ticker Symbol", value='TSLA')
# start_date = st.sidebar.date_input("Start Date", value=datetime(2020, 1, 1))
# end_date = st.sidebar.date_input("End Date", value=datetime.today())
# short_window = st.sidebar.slider("Short Window", min_value=10, max_value=100, value=50, step=1)
# long_window = st.sidebar.slider("Long Window", min_value=100, max_value=500, value=200, step=1)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    ticker = st.text_input("Ticker symbol", value="AAPL")
with col2:
    start_date = st.date_input("Start Date", value=datetime(2010,1,1), key="start_date2")
with col3:
    end_date = st.date_input("End Date", value=datetime.today(), key="end_date2")
with col4:
    short_window = st.slider("Short Window", min_value=10, max_value=100, value=50, step=1, key="short_window2")
with col5:
    long_window = st.slider("Long Window", min_value=100, max_value=500, value=200, step=1, key="long_window2")




# Main part of the script
if ticker and start_date and end_date:
    stock_data = get_stock_data(ticker, start_date, end_date)
    with st.expander("Simple Moving Average (SMA)", expanded=True):
        if stock_data is None:
            st.warning("No data found for the specified ticker and date range.")  # Display a warning message
        else:
            sma_strategy(stock_data, short_window=short_window, long_window=long_window)
            chart = plot_chart(stock_data, ticker)
            st.plotly_chart(chart)
else:
    st.warning("Please enter a valid ticker and date range.")


