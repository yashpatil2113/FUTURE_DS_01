"""
Data Generator Script for E-commerce Sales Dashboard
Generates realistic sample e-commerce data with 1000+ rows
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_ecommerce_data(num_records=1000):
    """
    Generate sample e-commerce dataset with realistic data
    
    Parameters:
    num_records (int): Number of records to generate (default: 1000)
    
    Returns:
    pd.DataFrame: Generated e-commerce dataset
    """
    
    # Product categories
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 
                  'Sports & Outdoors', 'Toys & Games', 'Health & Beauty', 
                  'Automotive', 'Food & Beverages', 'Office Supplies']
    
    # Sample product names by category
    products = {
        'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smart Watch', 
                       'Camera', 'Speaker', 'Monitor', 'Keyboard', 'Mouse'],
        'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Dress', 
                    'Shirt', 'Shorts', 'Hat', 'Socks', 'Belt'],
        'Home & Garden': ['Garden Tool', 'Plant Pot', 'Lawn Mower', 'Furniture', 
                         'Lamp', 'Curtains', 'Rug', 'Pillow', 'Blanket', 'Vase'],
        'Books': ['Novel', 'Textbook', 'Cookbook', 'Biography', 'Mystery', 
                 'Science Fiction', 'History', 'Poetry', 'Comic', 'Dictionary'],
        'Sports & Outdoors': ['Basketball', 'Tennis Racket', 'Yoga Mat', 'Dumbbells', 
                             'Bicycle', 'Running Shoes', 'Tent', 'Backpack', 'Helmet', 'Water Bottle'],
        'Toys & Games': ['Board Game', 'Action Figure', 'Puzzle', 'LEGO Set', 'Doll', 
                        'RC Car', 'Card Game', 'Building Blocks', 'Stuffed Animal', 'Art Set'],
        'Health & Beauty': ['Shampoo', 'Face Cream', 'Toothbrush', 'Vitamins', 'Perfume', 
                           'Makeup Kit', 'Hair Dryer', 'Razor', 'Sunscreen', 'Moisturizer'],
        'Automotive': ['Car Battery', 'Tire', 'Oil Filter', 'Brake Pad', 'Car Cover', 
                      'Floor Mat', 'Air Freshener', 'Phone Mount', 'Dash Cam', 'Tool Kit'],
        'Food & Beverages': ['Coffee', 'Tea', 'Chocolate', 'Snacks', 'Juice', 
                            'Cereal', 'Pasta', 'Sauce', 'Spices', 'Honey'],
        'Office Supplies': ['Notebook', 'Pen Set', 'Stapler', 'Folder', 'Binder', 
                           'Calculator', 'Desk Organizer', 'Paper Clips', 'Tape', 'Marker']
    }
    
    # Regions
    regions = ['North America', 'Europe', 'Asia Pacific', 'South America', 'Middle East', 'Africa']
    
    # Generate data
    data = []
    
    # Date range: last 2 years
    start_date = datetime.now() - timedelta(days=730)
    
    for i in range(num_records):
        # Generate OrderID
        order_id = f'ORD{str(i+1).zfill(6)}'
        
        # Select random category
        category = np.random.choice(categories)
        
        # Select random product from category
        product_name = np.random.choice(products[category])
        
        # Generate ProductID
        product_id = f'PROD{str(hash(product_name + category) % 10000).zfill(5)}'
        
        # Generate realistic price based on category
        base_prices = {
            'Electronics': (50, 2000),
            'Clothing': (10, 200),
            'Home & Garden': (15, 500),
            'Books': (5, 50),
            'Sports & Outdoors': (20, 800),
            'Toys & Games': (5, 150),
            'Health & Beauty': (3, 100),
            'Automotive': (10, 300),
            'Food & Beverages': (2, 50),
            'Office Supplies': (1, 100)
        }
        
        min_price, max_price = base_prices[category]
        price = round(np.random.uniform(min_price, max_price), 2)
        
        # Generate quantity (1-10 items per order)
        quantity = np.random.randint(1, 11)
        
        # Calculate revenue
        revenue = round(price * quantity, 2)
        
        # Generate random order date within last 2 years
        days_offset = np.random.randint(0, 730)
        order_date = start_date + timedelta(days=days_offset)
        
        # Generate CustomerID
        customer_id = f'CUST{str(np.random.randint(1, 501)).zfill(4)}'
        
        # Select random region
        region = np.random.choice(regions)
        
        data.append({
            'OrderID': order_id,
            'ProductID': product_id,
            'ProductName': product_name,
            'Category': category,
            'Quantity': quantity,
            'Price': price,
            'Revenue': revenue,
            'OrderDate': order_date,
            'CustomerID': customer_id,
            'Region': region
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Introduce some missing values (5% of records)
    missing_indices = np.random.choice(df.index, size=int(num_records * 0.05), replace=False)
    missing_cols = np.random.choice(['Price', 'Quantity', 'Region'], size=len(missing_indices))
    for idx, col in zip(missing_indices, missing_cols):
        df.loc[idx, col] = np.nan
    
    # Introduce some duplicates (2% of records)
    duplicate_indices = np.random.choice(df.index, size=int(num_records * 0.02), replace=False)
    duplicates = df.loc[duplicate_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    return df

if __name__ == '__main__':
    print("Generating e-commerce dataset...")
    
    # Generate 1000+ records
    df = generate_ecommerce_data(num_records=1200)
    
    # Save to CSV
    output_file = 'raw_ecommerce_data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Dataset generated successfully!")
    print(f"Total records: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"Data saved to: {output_file}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nData info:")
    print(df.info())
    print(f"\nMissing values:")
    print(df.isnull().sum())

