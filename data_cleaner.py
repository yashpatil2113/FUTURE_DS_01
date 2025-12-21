"""
Data Cleaning Script for E-commerce Sales Dashboard
Handles duplicates, missing values, data type conversions, and creates derived columns
"""

import pandas as pd
import numpy as np
from datetime import datetime

def clean_ecommerce_data(input_file='raw_ecommerce_data.csv', output_file='cleaned_ecommerce_data.csv'):
    """
    Clean and preprocess e-commerce data
    
    Parameters:
    input_file (str): Path to raw data CSV file
    output_file (str): Path to save cleaned data CSV file
    
    Returns:
    pd.DataFrame: Cleaned dataset
    """
    
    print("Loading raw data...")
    df = pd.read_csv(input_file)
    
    print(f"Initial records: {len(df)}")
    print(f"Initial columns: {list(df.columns)}")
    
    # Step 1: Remove duplicates
    print("\nStep 1: Removing duplicates...")
    initial_count = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_count - len(df)
    print(f"Removed {duplicates_removed} duplicate records")
    print(f"Records after deduplication: {len(df)}")
    
    # Step 2: Handle missing values
    print("\nStep 2: Handling missing values...")
    print("Missing values before cleaning:")
    print(df.isnull().sum())
    
    # Fill missing Price with median price for that category
    if df['Price'].isnull().any():
        category_medians = df.groupby('Category')['Price'].median()
        df['Price'] = df.apply(
            lambda row: category_medians[row['Category']] if pd.isnull(row['Price']) else row['Price'],
            axis=1
        )
        print(f"Filled {df['Price'].isnull().sum()} missing prices with category medians")
    
    # Fill missing Quantity with 1 (minimum order quantity)
    if df['Quantity'].isnull().any():
        df['Quantity'] = df['Quantity'].fillna(1)
        print(f"Filled {df['Quantity'].isnull().sum()} missing quantities with 1")
    
    # Fill missing Region with 'Unknown'
    if df['Region'].isnull().any():
        df['Region'] = df['Region'].fillna('Unknown')
        print(f"Filled {df['Region'].isnull().sum()} missing regions with 'Unknown'")
    
    # Recalculate Revenue if Price or Quantity were missing
    df['Revenue'] = df['Price'] * df['Quantity']
    
    print("Missing values after cleaning:")
    print(df.isnull().sum())
    
    # Step 3: Convert data types
    print("\nStep 3: Converting data types...")
    
    # Convert OrderDate to datetime
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    print("Converted OrderDate to datetime")
    
    # Ensure numeric columns are correct types
    df['Quantity'] = df['Quantity'].astype(int)
    df['Price'] = df['Price'].astype(float)
    df['Revenue'] = df['Revenue'].astype(float)
    print("Converted Quantity, Price, and Revenue to appropriate numeric types")
    
    # Ensure string columns are object type
    string_columns = ['OrderID', 'ProductID', 'ProductName', 'Category', 'CustomerID', 'Region']
    for col in string_columns:
        df[col] = df[col].astype(str)
    print("Converted string columns to object type")
    
    # Step 4: Create derived columns
    print("\nStep 4: Creating derived columns...")
    
    # Total Sales (same as Revenue, but kept for clarity)
    df['TotalSales'] = df['Revenue']
    print("Created TotalSales column")
    
    # Profit Margin (assume 20-40% profit margin based on category)
    profit_margins = {
        'Electronics': 0.25,
        'Clothing': 0.35,
        'Home & Garden': 0.30,
        'Books': 0.40,
        'Sports & Outdoors': 0.30,
        'Toys & Games': 0.35,
        'Health & Beauty': 0.40,
        'Automotive': 0.25,
        'Food & Beverages': 0.20,
        'Office Supplies': 0.30
    }
    
    df['ProfitMargin'] = df['Category'].map(profit_margins)
    df['Profit'] = df['Revenue'] * df['ProfitMargin']
    print("Created ProfitMargin and Profit columns")
    
    # Extract date components for time-based analysis
    df['Year'] = df['OrderDate'].dt.year
    df['Month'] = df['OrderDate'].dt.month
    df['Quarter'] = df['OrderDate'].dt.quarter
    df['MonthName'] = df['OrderDate'].dt.strftime('%B')
    df['YearMonth'] = df['OrderDate'].dt.to_period('M').astype(str)
    print("Created date component columns (Year, Month, Quarter, MonthName, YearMonth)")
    
    # Calculate days since order (for recency analysis)
    current_date = datetime.now()
    df['DaysSinceOrder'] = (current_date - df['OrderDate']).dt.days
    print("Created DaysSinceOrder column")
    
    # Step 5: Data validation and outlier handling
    print("\nStep 5: Data validation...")
    
    # Remove any negative values in Price, Quantity, or Revenue
    initial_count = len(df)
    df = df[(df['Price'] > 0) & (df['Quantity'] > 0) & (df['Revenue'] > 0)]
    removed = initial_count - len(df)
    if removed > 0:
        print(f"Removed {removed} records with invalid values")
    
    # Remove extreme outliers (Price > 3 standard deviations from mean)
    for category in df['Category'].unique():
        category_data = df[df['Category'] == category]
        mean_price = category_data['Price'].mean()
        std_price = category_data['Price'].std()
        upper_limit = mean_price + (3 * std_price)
        lower_limit = mean_price - (3 * std_price)
        
        outliers = df[(df['Category'] == category) & 
                     ((df['Price'] > upper_limit) | (df['Price'] < lower_limit))]
        if len(outliers) > 0:
            df = df[~((df['Category'] == category) & 
                     ((df['Price'] > upper_limit) | (df['Price'] < lower_limit)))]
            print(f"Removed {len(outliers)} price outliers from {category}")
    
    # Step 6: Final data summary
    print("\n" + "="*50)
    print("Data Cleaning Summary")
    print("="*50)
    print(f"Final records: {len(df)}")
    print(f"Final columns: {list(df.columns)}")
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nMissing values:")
    print(df.isnull().sum())
    print(f"\nBasic statistics:")
    print(df[['Quantity', 'Price', 'Revenue', 'Profit']].describe())
    
    # Step 7: Save cleaned data
    print(f"\nSaving cleaned data to {output_file}...")
    df.to_csv(output_file, index=False)
    print("Data cleaning completed successfully!")
    
    return df

if __name__ == '__main__':
    # Clean the data
    cleaned_df = clean_ecommerce_data()
    
    print("\nFirst few rows of cleaned data:")
    print(cleaned_df.head(10))

