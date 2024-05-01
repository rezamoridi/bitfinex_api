import pandas as pd
import plotly.graph_objects as go


# Create DataFrame from CSV data
df = pd.read_csv("/home/gh/Desktop/BTCUSD-2024-04-08-2024-04-11-1h.csv")

# Convert Timestamp column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Create the plot
fig = go.Figure()

# Candlestick trace
fig.add_trace(go.Candlestick(x=df['Timestamp'],
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             name='Candlestick'))

# Add volume bars as separate trace
fig.add_trace(go.Bar(x=df['Timestamp'], y=df['Volume'], name='Volume', marker_color='blue', opacity=0.5))

# Update layout
fig.update_layout(title='Stock Price and Volume',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  #yaxis2_title='Volume',
                  yaxis2=dict(anchor='x', overlaying='y', side='right'))

# Show the plot
fig.show()
