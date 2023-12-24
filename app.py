import os
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

# Load CPI data
cpi_data = pd.read_excel("CPI.xlsx")
cpi_data['Date'] = pd.to_datetime(cpi_data['Date'])
cpi_data.set_index('Date', inplace=True)

# Load stock data
stock_folder = "stock_folder"
stock_files = [f for f in os.listdir(stock_folder) if f.endswith(".xlsx")]

# Function to calculate correlation and build linear regression model
def analyze_stock(stock_data, cpi_data):
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data.set_index('Date', inplace=True)
    
    # Merge stock and CPI data on Date
    merged_data = pd.merge(stock_data, cpi_data, left_index=True, right_index=True, how='inner')
    
    # Drop NaN values
    merged_data = merged_data.dropna()

    # Show line chart with close price in blue and CPI in red
    st.write("\nLine Chart - Close Price (Blue) and CPI (Red):")
    plt.figure(figsize=(10, 6))
    plt.plot(merged_data.index, merged_data['Close'], label='Close Price', color='blue')
    plt.plot(merged_data.index, merged_data['CPI'], label='CPI', color='red')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Line Chart - Close Price and CPI')
    plt.legend()
    st.pyplot()

# Streamlit UI
st.title("Stock-CPI Line Chart - Close Price and CPI")
selected_stock = st.selectbox("Select Stock", stock_files)

# Load selected stock data
selected_stock_data = pd.read_excel(os.path.join(stock_folder, selected_stock))
analyze_stock(selected_stock_data, cpi_data)
