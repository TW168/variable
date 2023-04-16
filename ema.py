import pandas as pd
import yfinance as yf
import plotly.graph_objs as go



# Calculate EMA
def calculate_ema(data, ema_window):
    data[f"EMA{ema_window}"] = data["Close"].ewm(span=ema_window).mean()

# Plot stock prices and EMA using plotly
def plot_ema_chart(stock_data, ticker, ema_window):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name="Close"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data[f"EMA{ema_window}"], mode="lines", name=f"EMA{ema_window}"))

    fig.update_layout(title=f"{ticker} Price and EMA{ema_window}",
                      xaxis_title="Date",
                      yaxis_title="Price",
                      legend_title="Indicators")

    return fig