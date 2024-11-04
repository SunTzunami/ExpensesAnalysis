import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
from datetime import datetime
import numpy as np
from plotters import plot_category_distribution, plot_sunburst, plot_cumulative_expense, plot_expense_timeseries

# Set page config
st.set_page_config(page_title="Expense Analyzer", layout="wide")

# Title and description
st.title("💰 Expense Analysis Dashboard")
st.write("Upload your expense data and analyze spending patterns")

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("Upload Expense Data (Excel)", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        # Read the data
        df = pd.read_excel(uploaded_file)
        
        # Convert Date column to datetime if not already
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Ensure category column is string type
        df['category'] = df['category'].astype(str)
        
        # Selection options for date filtering
        analysis_type = st.radio("Select Analysis Type", ["Year", "Month", "Day", "Custom Range"])
        
        if analysis_type == "Year":
            available_years = sorted(df['Date'].dt.year.unique())
            selected_year = st.selectbox("Select Year", available_years)
            df_filtered = df[df['Date'].dt.year == selected_year].copy()
            period_text = f"Year {selected_year}"
        
        elif analysis_type == "Month":
            available_years = sorted(df['Date'].dt.year.unique())
            selected_year = st.selectbox("Select Year", available_years)
            available_months = sorted(df[df['Date'].dt.year == selected_year]['Date'].dt.month.unique())
            month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                           7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
            month_name_options = [month_names[month] for month in available_months]
            selected_month_name = st.selectbox("Select Month", month_name_options)
            selected_month = [k for k, v in month_names.items() if v == selected_month_name][0]
            df_filtered = df[(df['Date'].dt.year == selected_year) & (df['Date'].dt.month == selected_month)].copy()
            period_text = f"{selected_month_name} {selected_year}"
        
        elif analysis_type == "Day":
            selected_date = st.date_input("Select Date")
            df_filtered = df[df['Date'] == pd.to_datetime(selected_date)].copy()
            period_text = f"Date {selected_date.strftime('%Y-%m-%d')}"
        
        elif analysis_type == "Custom Range":
            start_date = st.date_input("Start Date", value=df['Date'].min())
            end_date = st.date_input("End Date", value=df['Date'].max())
            if start_date > end_date:
                st.error("End Date should be after Start Date")
            else:
                df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))].copy()
                period_text = f"Period {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        
        # Add dynamic title based on selected period
        st.subheader(f"Analysis for {period_text}")
        
        # Category grouping option
        st.subheader("Category Settings")
        use_default_categories = st.checkbox("Use Default Category Grouping", value=True)
        
        # Plotly publishing option
        st.subheader("Export Settings")
        enable_plotly_export = st.checkbox("Enable Plotly Export", value=False)

# Main content area
if 'df_filtered' in locals() and not df_filtered.empty:
    # Apply default category mapping if selected
    if use_default_categories:
        category_mapping = {
            'grocery': 'Food', 'Grocery': 'Food', 'snacks': 'Food', 'Snacks': 'Food',
            'dining': 'Food', 'Dining': 'Food', 'medicines': 'Personal Care and Medicines',
            'Medicines': 'Personal Care and Medicines', 'personal care': 'Personal Care and Medicines',
            'Personal care': 'Personal Care and Medicines', 'misc': 'Miscellaneous',
            'Misc': 'Miscellaneous', 'entertainment': 'Entertainment and Books', 'Entertainment': 'Entertainment and Books',
            'books': 'Entertainment and Books', 'Books': 'Entertainment and Books', 'housing': 'Housing and Utilities',
            'Housing': 'Housing and Utilities', 'utility': 'Housing and Utilities', 'Utility': 'Housing and Utilities',
            'clothing': 'Household and Clothing', 'Clothing': 'Household and Clothing', 'household': 'Household and Clothing',
            'Household': 'Household and Clothing', 'furniture': 'Electronics and Furniture', 'Furniture': 'Electronics and Furniture',
            'electronics': 'Electronics and Furniture', 'Electronics': 'Electronics and Furniture', 'supplements': 'Fitness',
            'Supplements': 'Fitness', 'shoes': 'Fitness', 'Shoes': 'Fitness', 'sports event': 'Fitness', 'Sports event': 'Fitness',
            'sports watch': 'Fitness', 'Sports watch': 'Fitness', 'sports clothing': 'Fitness', 'Sports clothing': 'Fitness',
            'sports rental': 'Fitness', 'Sports rental': 'Fitness', 'gym': 'Fitness', 'Gym': 'Fitness', 'sports equipment': 'Fitness',
            'Sports equipment': 'Fitness', 'commute': 'Transportation', 'Commute': 'Transportation', 'ride share': 'Transportation',
            'Ride share': 'Transportation', 'tokyo metro': 'Transportation', 'Tokyo Metro': 'Transportation', 'flight tickets': 'Transportation',
            'Flight tickets': 'Transportation', 'souvenirs': 'Souvenirs/Gifts/Treats', 'Souvenirs': 'Souvenirs/Gifts/Treats',
            'treat': 'Souvenirs/Gifts/Treats', 'Treat': 'Souvenirs/Gifts/Treats', 'gift': 'Souvenirs/Gifts/Treats', 'Gift': 'Souvenirs/Gifts/Treats'
        }
        
        # Create NewCategory column
        df_filtered['NewCategory'] = df_filtered['category'].map(category_mapping)
        df_filtered['NewCategory'] = df_filtered['NewCategory'].fillna(df_filtered['category'])
    else:
        df_filtered['NewCategory'] = df_filtered['category']

    # Data Processing
    df_filtered = df_filtered[df_filtered['Expense'] != 0]
    
    # Calculate total expenses, average monthly, and daily expenses
    period_days = (df_filtered['Date'].max() - df_filtered['Date'].min()).days + 1
    period_months = period_days / 30
    total_expense = df_filtered['Expense'].sum()
    average_monthly_expense = total_expense / period_months
    average_daily_expense = total_expense / period_days

    # Display Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Expenses", f"¥{total_expense:,.0f}")
    with col2:
        st.metric("Average Monthly Expense", f"¥{average_monthly_expense:,.0f}")
    with col3:
        st.metric("Average Daily Expense", f"¥{average_daily_expense:,.0f}")

    # Display plots in columns
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_category_distribution(df_filtered), use_container_width=True)
    with col2:
        st.plotly_chart(plot_sunburst(df_filtered), use_container_width=True)

    # Display Cumulative Expense Plot
    st.plotly_chart(plot_cumulative_expense(df_filtered), use_container_width=True)

    # Display Timeseries Expense Plot
    st.plotly_chart(plot_expense_timeseries(df_filtered), use_container_width=True)

else:
    st.info("Please upload an expense file to begin analysis")
