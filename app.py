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
    
    # Calculate percentage change
    merged_data['Close % Change'] = merged_data['Close'].pct_change() * 100
    merged_data['CPI % Change'] = merged_data['CPI'].pct_change() * 100
    
    # Drop NaN values
    merged_data = merged_data.dropna()

    # Show percentage change comparison
    st.write("\nPercentage Change Comparison:")
    st.dataframe(merged_data[['Close % Change', 'CPI % Change']])

    # Show scatter plot
    st.write("\nScatter Plot - Percentage Change Comparison:")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='CPI % Change', y='Close % Change', data=merged_data)
    plt.xlabel('CPI % Change')
    plt.ylabel('Close % Change')
    plt.title('Scatter Plot - Percentage Change Comparison')
    st.pyplot()

# Streamlit UI
st.title("Stock-CPI Percentage Change Comparison")
selected_stock = st.selectbox("Select Stock", stock_files)

# Load selected stock data
selected_stock_data = pd.read_excel(os.path.join(stock_folder, selected_stock))
analyze_stock(selected_stock_data, cpi_data)
