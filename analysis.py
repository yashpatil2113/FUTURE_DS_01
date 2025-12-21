"""
Analysis Script for E-commerce Sales Dashboard
Performs key calculations and generates insights for Power BI
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_cleaned_data(file_path='cleaned_ecommerce_data.csv'):
    """
    Load cleaned e-commerce data
    
    Parameters:
    file_path (str): Path to cleaned data CSV file
    
    Returns:
    pd.DataFrame: Loaded dataset
    """
    print(f"Loading cleaned data from {file_path}...")
    df = pd.read_csv(file_path, parse_dates=['OrderDate'])
    print(f"Loaded {len(df)} records")
    return df

def calculate_total_sales_revenue(df):
    """
    Calculate total sales and revenue metrics
    
    Parameters:
    df (pd.DataFrame): E-commerce dataset
    
    Returns:
    dict: Dictionary containing total sales metrics
    """
    print("\n" + "="*60)
    print("TOTAL SALES AND REVENUE ANALYSIS")
    print("="*60)
    
    total_revenue = df['Revenue'].sum()
    total_sales = df['TotalSales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['OrderID'].nunique()
    total_products_sold = df['Quantity'].sum()
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    results = {
        'Total Revenue': round(total_revenue, 2),
        'Total Sales': round(total_sales, 2),
        'Total Profit': round(total_profit, 2),
        'Total Orders': total_orders,
        'Total Products Sold': int(total_products_sold),
        'Average Order Value': round(average_order_value, 2)
    }
    
    for key, value in results.items():
        print(f"{key}: {value:,}" if isinstance(value, (int, float)) else f"{key}: {value}")
    
    return results

def find_best_selling_products(df, top_n=10):
    """
    Find top N best-selling products by quantity and revenue
    
    Parameters:
    df (pd.DataFrame): E-commerce dataset
    top_n (int): Number of top products to return
    
    Returns:
    tuple: (top_by_quantity, top_by_revenue) DataFrames
    """
    print("\n" + "="*60)
    print(f"BEST-SELLING PRODUCTS (TOP {top_n})")
    print("="*60)
    
    # Top products by quantity sold
    top_by_quantity = df.groupby(['ProductID', 'ProductName', 'Category']).agg({
        'Quantity': 'sum',
        'Revenue': 'sum',
        'OrderID': 'nunique'
    }).reset_index()
    top_by_quantity.columns = ['ProductID', 'ProductName', 'Category', 'TotalQuantity', 'TotalRevenue', 'OrderCount']
    top_by_quantity = top_by_quantity.sort_values('TotalQuantity', ascending=False).head(top_n)
    
    # Top products by revenue
    top_by_revenue = df.groupby(['ProductID', 'ProductName', 'Category']).agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'OrderID': 'nunique'
    }).reset_index()
    top_by_revenue.columns = ['ProductID', 'ProductName', 'Category', 'TotalRevenue', 'TotalQuantity', 'OrderCount']
    top_by_revenue = top_by_revenue.sort_values('TotalRevenue', ascending=False).head(top_n)
    
    print("\nTop Products by Quantity Sold:")
    print(top_by_quantity[['ProductName', 'Category', 'TotalQuantity', 'TotalRevenue']].to_string(index=False))
    
    print("\nTop Products by Revenue:")
    print(top_by_revenue[['ProductName', 'Category', 'TotalRevenue', 'TotalQuantity']].to_string(index=False))
    
    return top_by_quantity, top_by_revenue

def analyze_high_revenue_categories(df):
    """
    Analyze revenue by category
    
    Parameters:
    df (pd.DataFrame): E-commerce dataset
    
    Returns:
    pd.DataFrame: Category revenue analysis
    """
    print("\n" + "="*60)
    print("HIGH-REVENUE CATEGORIES")
    print("="*60)
    
    category_analysis = df.groupby('Category').agg({
        'Revenue': ['sum', 'mean'],
        'Quantity': 'sum',
        'OrderID': 'nunique',
        'Profit': 'sum'
    }).reset_index()
    
    category_analysis.columns = ['Category', 'TotalRevenue', 'AvgRevenue', 'TotalQuantity', 'OrderCount', 'TotalProfit']
    category_analysis['RevenuePercentage'] = (category_analysis['TotalRevenue'] / category_analysis['TotalRevenue'].sum() * 100).round(2)
    category_analysis = category_analysis.sort_values('TotalRevenue', ascending=False)
    
    print(category_analysis.to_string(index=False))
    
    return category_analysis

def analyze_sales_trends(df):
    """
    Analyze monthly and quarterly sales trends
    
    Parameters:
    df (pd.DataFrame): E-commerce dataset
    
    Returns:
    tuple: (monthly_trends, quarterly_trends) DataFrames
    """
    print("\n" + "="*60)
    print("SALES TRENDS ANALYSIS")
    print("="*60)
    
    # Monthly trends
    monthly_trends = df.groupby('YearMonth').agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'OrderID': 'nunique',
        'Profit': 'sum'
    }).reset_index()
    monthly_trends.columns = ['YearMonth', 'TotalRevenue', 'TotalQuantity', 'OrderCount', 'TotalProfit']
    monthly_trends = monthly_trends.sort_values('YearMonth')
    
    print("\nMonthly Sales Trends:")
    print(monthly_trends.to_string(index=False))
    
    # Quarterly trends
    quarterly_trends = df.groupby(['Year', 'Quarter']).agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'OrderID': 'nunique',
        'Profit': 'sum'
    }).reset_index()
    quarterly_trends.columns = ['Year', 'Quarter', 'TotalRevenue', 'TotalQuantity', 'OrderCount', 'TotalProfit']
    quarterly_trends['YearQuarter'] = quarterly_trends['Year'].astype(str) + '-Q' + quarterly_trends['Quarter'].astype(str)
    quarterly_trends = quarterly_trends.sort_values(['Year', 'Quarter'])
    
    print("\nQuarterly Sales Trends:")
    print(quarterly_trends[['YearQuarter', 'TotalRevenue', 'TotalQuantity', 'OrderCount']].to_string(index=False))
    
    return monthly_trends, quarterly_trends

def calculate_average_order_value(df):
    """
    Calculate average order value and related metrics
    
    Parameters:
    df (pd.DataFrame): E-commerce dataset
    
    Returns:
    dict: Dictionary containing AOV metrics
    """
    print("\n" + "="*60)
    print("AVERAGE ORDER VALUE (AOV) ANALYSIS")
    print("="*60)
    
    # Overall AOV
    order_totals = df.groupby('OrderID')['Revenue'].sum()
    overall_aov = order_totals.mean()
    
    # AOV by category
    category_aov = df.groupby('Category').apply(
        lambda x: x.groupby('OrderID')['Revenue'].sum().mean(),
        include_groups=False
    ).reset_index()
    category_aov.columns = ['Category', 'AverageOrderValue']
    category_aov = category_aov.sort_values('AverageOrderValue', ascending=False)
    
    # AOV by region
    region_aov = df.groupby('Region').apply(
        lambda x: x.groupby('OrderID')['Revenue'].sum().mean(),
        include_groups=False
    ).reset_index()
    region_aov.columns = ['Region', 'AverageOrderValue']
    region_aov = region_aov.sort_values('AverageOrderValue', ascending=False)
    
    results = {
        'Overall AOV': round(overall_aov, 2),
        'Category AOV': category_aov,
        'Region AOV': region_aov
    }
    
    print(f"Overall Average Order Value: ${overall_aov:,.2f}")
    print("\nAOV by Category:")
    print(category_aov.to_string(index=False))
    print("\nAOV by Region:")
    print(region_aov.to_string(index=False))
    
    return results

def generate_regional_analysis(df):
    """
    Analyze sales by region
    
    Parameters:
    df (pd.DataFrame): E-commerce dataset
    
    Returns:
    pd.DataFrame: Regional analysis
    """
    print("\n" + "="*60)
    print("REGIONAL ANALYSIS")
    print("="*60)
    
    regional_analysis = df.groupby('Region').agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'OrderID': 'nunique',
        'CustomerID': 'nunique',
        'Profit': 'sum'
    }).reset_index()
    regional_analysis.columns = ['Region', 'TotalRevenue', 'TotalQuantity', 'OrderCount', 'CustomerCount', 'TotalProfit']
    regional_analysis['RevenuePercentage'] = (regional_analysis['TotalRevenue'] / regional_analysis['TotalRevenue'].sum() * 100).round(2)
    regional_analysis = regional_analysis.sort_values('TotalRevenue', ascending=False)
    
    print(regional_analysis.to_string(index=False))
    
    return regional_analysis

def export_analysis_results(df, output_dir='analysis_output'):
    """
    Export analysis results to CSV files for Power BI
    
    Parameters:
    df (pd.DataFrame): E-commerce dataset
    output_dir (str): Directory to save analysis results
    """
    import os
    
    print("\n" + "="*60)
    print("EXPORTING ANALYSIS RESULTS")
    print("="*60)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Export best-selling products
    top_by_quantity, top_by_revenue = find_best_selling_products(df, top_n=10)
    top_by_quantity.to_csv(f'{output_dir}/top_products_by_quantity.csv', index=False)
    top_by_revenue.to_csv(f'{output_dir}/top_products_by_revenue.csv', index=False)
    
    # Export category analysis
    category_analysis = analyze_high_revenue_categories(df)
    category_analysis.to_csv(f'{output_dir}/category_analysis.csv', index=False)
    
    # Export sales trends
    monthly_trends, quarterly_trends = analyze_sales_trends(df)
    monthly_trends.to_csv(f'{output_dir}/monthly_trends.csv', index=False)
    quarterly_trends.to_csv(f'{output_dir}/quarterly_trends.csv', index=False)
    
    # Export regional analysis
    regional_analysis = generate_regional_analysis(df)
    regional_analysis.to_csv(f'{output_dir}/regional_analysis.csv', index=False)
    
    # Export AOV analysis
    aov_results = calculate_average_order_value(df)
    aov_results['Category AOV'].to_csv(f'{output_dir}/aov_by_category.csv', index=False)
    aov_results['Region AOV'].to_csv(f'{output_dir}/aov_by_region.csv', index=False)
    
    print(f"\nAll analysis results exported to '{output_dir}' directory")

def run_complete_analysis():
    """
    Run complete analysis pipeline
    """
    print("="*60)
    print("E-COMMERCE SALES DASHBOARD - COMPLETE ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_cleaned_data()
    
    # Run all analyses
    total_metrics = calculate_total_sales_revenue(df)
    find_best_selling_products(df, top_n=10)
    analyze_high_revenue_categories(df)
    analyze_sales_trends(df)
    calculate_average_order_value(df)
    generate_regional_analysis(df)
    
    # Export results
    export_analysis_results(df)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print("\nKey Insights Summary:")
    print(f"- Total Revenue: ${total_metrics['Total Revenue']:,.2f}")
    print(f"- Total Orders: {total_metrics['Total Orders']:,}")
    print(f"- Average Order Value: ${total_metrics['Average Order Value']:,.2f}")
    print(f"- Total Products Sold: {total_metrics['Total Products Sold']:,}")

if __name__ == '__main__':
    run_complete_analysis()

