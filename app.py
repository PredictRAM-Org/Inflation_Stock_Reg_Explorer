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
    y = merged_data['CPI Change']

    # Train linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Show correlation with each stock
    correlation_results = {}
    for column in merged_data.columns[:-2]:  # Exclude 'CPI Change' and 'CPI' columns
        stock_column = merged_data[column]
        correlation = stock_column.corr(merged_data['CPI Change'])
        correlation_results[column] = correlation

    # Display results
    st.write("\nCorrelation with CPI Change:")
    for stock, correlation in correlation_results.items():
        st.write(f"{stock}: {correlation}")

    # Show correlation heatmap
    correlation_matrix = merged_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    st.pyplot()

# Streamlit UI
st.title("Stock-CPI Correlation Analysis")
train_model_button = st.button("Train Model")

if train_model_button:
    st.write("Training model...")

    for stock_file in stock_files:
        st.write(f"\nCorrelation for {stock_file}:")
        selected_stock_data = pd.read_excel(os.path.join(stock_folder, stock_file))
        analyze_stock(selected_stock_data, cpi_data)
