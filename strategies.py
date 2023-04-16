from datetime import datetime, timedelta
import streamlit as st
from sma import get_stock_data, sma_strategy, plot_chart
from ema import calculate_ema, plot_ema_chart

# Set page configuration
st.set_page_config(page_title="Strategies", page_icon="📈", layout="wide")


def main():
    # Display title
    st.title("Strategies")
    st.markdown("<p style='font-size: 10px;'>* Use this at your own risk</p>", unsafe_allow_html=True)

    # Input fields for user to enter data
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        ticker = st.text_input("Ticker symbol", value="AAPL")
    with col2:
        start_date = st.date_input(
            "Start Date", value=datetime(2010, 1, 1), key="start_date2"
        )
    with col3:
        end_date = st.date_input("End Date", value=datetime.today(), key="end_date2")
    with col4:
        short_window = st.slider(
            "Short Window",
            min_value=10,
            max_value=100,
            value=50,
            step=1,
            key="short_window2",
        )
    with col5:
        long_window = st.slider(
            "Long Window",
            min_value=100,
            max_value=500,
            value=200,
            step=1,
            key="long_window2",
        )
        ema_window = st.slider("EMA Window", 5, 200, 20)

    # Check if provided a ticker and vaild date range
    if ticker and start_date and end_date:
        # Fetch the stock data for the specified ticker and date range, this function is in sma.py
        stock_data = get_stock_data(ticker, start_date, end_date)
        # Check if the stock data is available
        if stock_data is None:
            st.warning(
                "No data found for the specified ticker and date range."
            )  # Display a warning message
        else:
            # Create an expander with two columns inside
            with st.expander("Common Stategies", expanded=True):
                col1, col2 = st.columns(2)
            # Column 1: Display the stock chart with SMA strategy
            with col1:
                sma_strategy(
                    stock_data, short_window=short_window, long_window=long_window
                )
                chart = plot_chart(stock_data, ticker)
                st.plotly_chart(chart)
                st.write(" For example, if the closing price of the stock is above the 50-day SMA, this could be a bullish signal, indicating that the stock is in an uptrend. Conversely, if the closing price is below the 50-day SMA, this could be a bearish signal, indicating that the stock is in a downtrend.")
            # Column 2: Display the stock chart with EMA strategy
            with col2:
                calculate_ema(stock_data, ema_window)
                ema_chart = plot_ema_chart(stock_data, ticker, ema_window)
                st.plotly_chart(ema_chart, ema_window)
                st.write(
                    "For example, a trader might use the EMA to identify a bullish trend when the closing price is above the EMA and the EMA is sloping upward. Alternatively, a bearish trend could be identified when the closing price is below the EMA and the EMA is sloping downward. The EMA can also be used to identify potential areas of support or resistance, where prices may bounce off the EMA or break through it."
                )
            with st.expander("Coming Soon"):
                st.write("Prediction")
    else:
        # Display a warning message if hasn't provided a valid ticker and date range
        st.warning("Please enter a valid ticker and date range.")


if __name__ == "__main__":
    main()
