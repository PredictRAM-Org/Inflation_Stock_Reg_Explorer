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
def analyze_stock(stock_data, cpi_data, future_inflation):
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

    # Predict future inflation
    future_inflation_prediction = model.predict([[future_inflation]])
    st.write(f"Predicted CPI Change for Future Inflation ({future_inflation}): {future_inflation_prediction[0]}")

    # Show correlation with actual CPI Change
    correlation_results_actual = {}
    for column in merged_data.columns[:-2]:  # Exclude 'CPI Change' and 'CPI' columns
        stock_column = merged_data[column]
        correlation = stock_column.corr(merged_data['CPI Change'])
        correlation_results_actual[column] = correlation

    # Show correlation with predicted CPI Change
    correlation_results_predicted = {}
    for column in merged_data.columns[:-2]:  # Exclude 'CPI Change' and 'CPI' columns
        stock_column = merged_data[column]
        correlation = stock_column.corr(pd.Series(future_inflation_prediction[0], index=stock_column.index))
        correlation_results_predicted[column] = correlation

    # Display results
    st.write("\nCorrelation with Actual CPI Change:")
    for stock, correlation in correlation_results_actual.items():
        st.write(f"{stock}: {correlation}")

    st.write("\nCorrelation with Predicted CPI Change:")
    for stock, correlation in correlation_results_predicted.items():
        st.write(f"{stock}: {correlation}")

    # Show correlation heatmap
    correlation_matrix = merged_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    st.pyplot()

# Streamlit UI
st.title("Stock-CPI Correlation and Prediction Analysis")
selected_stock = st.selectbox("Select Stock", stock_files)
future_inflation_input = st.number_input("Enter Expected Future Inflation:", min_value=0.0, step=0.01)
train_model_button = st.button("Train Model")

# Load selected stock data
selected_stock_data = pd.read_excel(os.path.join(stock_folder, selected_stock))

# Train the model if the button is clicked
if train_model_button:
    st.write("Training model...")
    analyze_stock(selected_stock_data, cpi_data, future_inflation_input)
