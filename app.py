import os
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load CPI data
cpi_data = pd.read_excel("CPI.xlsx")
cpi_data['Date'] = pd.to_datetime(cpi_data['Date'])
cpi_data.set_index('Date', inplace=True)

# Load stock data
stock_folder = "stock_folder"
stock_files = [f for f in os.listdir(stock_folder) if f.endswith(".xlsx")]

# Function to calculate correlation and build regression model
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
    X = merged_data.drop(['CPI Change'], axis=1)
    y = merged_data['CPI Change']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train models
    models = {
        'Random Forest': RandomForestRegressor(),
        'SVM': SVR(),
        'Neural Network': MLPRegressor()
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        st.write(f"{name} Mean Squared Error: {mse}")

    # Show correlation heatmap
    correlation_matrix = merged_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    st.pyplot()

# Streamlit UI
st.title("Stock-CPI Correlation Analysis")
selected_stock = st.selectbox("Select Stock", stock_files)

# Load selected stock data
selected_stock_data = pd.read_excel(os.path.join(stock_folder, selected_stock))
analyze_stock(selected_stock_data, cpi_data)
