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
    
    # Calculate CPI change
    merged_data['CPI Change'] = merged_data['CPI'].pct_change()
    
    # Drop NaN values
    merged_data = merged_data.dropna()

    # Features and target
    X = merged_data[['CPI']]
    y = merged_data['Close']

    # Train linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict close price based on CPI
    merged_data['Predicted Close'] = model.predict(merged_data[['CPI']])

    # Show correlation line chart
    st.line_chart(merged_data[['Close', 'CPI']])

# Streamlit UI
st.title("Stock-CPI Correlation Line Chart")
selected_stock = st.selectbox("Select Stock", stock_files)

# Load selected stock data
selected_stock_data = pd.read_excel(os.path.join(stock_folder, selected_stock))
analyze_stock(selected_stock_data, cpi_data)
