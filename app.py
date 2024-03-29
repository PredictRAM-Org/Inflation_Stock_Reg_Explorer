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
def analyze_stock(stock_data, cpi_data, expected_inflation):
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data.set_index('Date', inplace=True)
    
    # Merge stock and CPI data on Date
    merged_data = pd.merge(stock_data, cpi_data, left_index=True, right_index=True, how='inner')
    
    # Handle NaN values in CPI column
    if merged_data['CPI'].isnull().any():
        st.write(f"Warning: NaN values found in 'CPI' column for {stock_data.name}. Dropping NaN values.")
        merged_data = merged_data.dropna(subset=['CPI'])

    # Calculate CPI change
    merged_data['CPI Change'] = merged_data['CPI'].pct_change()

    # Drop NaN values after calculating percentage change
    merged_data = merged_data.dropna()

    # Show correlation between 'Close' column and 'CPI Change'
    correlation_close_cpi = merged_data['Close'].corr(merged_data['CPI Change'])
    st.write(f"Correlation between 'Close' and 'CPI Change' for {stock_data.name}: {correlation_close_cpi}")

    # Calculate the adjusted correlation based on expected inflation impact
    adjusted_correlation = correlation_close_cpi + 0.1 * expected_inflation  # You can adjust the multiplier as needed
    st.write(f"Adjusted Correlation with Expected Inflation ({expected_inflation}): {adjusted_correlation}")

    return correlation_close_cpi, adjusted_correlation

# Streamlit UI
st.title("Stock-CPI Correlation Analysis with Expected Inflation")
expected_inflation = st.number_input("Enter Expected Upcoming Inflation:", min_value=0.0, step=0.01)
train_model_button = st.button("Train Model")

if train_model_button:
    st.write(f"Training model with Expected Inflation: {expected_inflation}...")
    
    actual_correlations = []
    expected_correlations = []
    stock_names = []

    for stock_file in stock_files:
        st.write(f"\nTraining for {stock_file}...")
        selected_stock_data = pd.read_excel(os.path.join(stock_folder, stock_file))
        selected_stock_data.name = stock_file  # Assign a name to the stock_data for reference
        actual_corr, expected_corr = analyze_stock(selected_stock_data, cpi_data, expected_inflation)
        
        actual_correlations.append(actual_corr)
        expected_correlations.append(expected_corr)
        stock_names.append(stock_file)

    # Display overall summary in a table
    summary_data = {
        'Stock': stock_names,
        'Actual Correlation': actual_correlations,
        f'Expected Correlation (Inflation={expected_inflation})': expected_correlations
    }
    summary_df = pd.DataFrame(summary_data)
    st.write("\nCorrelation Summary:")
    st.table(summary_df)

    # Display overall summary in a column format
    st.write("\nCorrelation Summary (Column Format):")
    for stock, actual_corr, expected_corr in zip(stock_names, actual_correlations, expected_correlations):
        st.write(f"{stock}:")
        st.write(f"  - Actual Correlation: {actual_corr}")
        st.write(f"  - Expected Correlation (Inflation={expected_inflation}): {expected_corr}")
