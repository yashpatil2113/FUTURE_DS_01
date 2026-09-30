# Business Sales Dashboard - E-commerce Analysis Project

A complete e-commerce sales analysis project designed for Power BI integration. This project generates realistic sample data, cleans and preprocesses it, and performs comprehensive sales analytics.

## 📋 Project Overview

This project provides a complete pipeline for analyzing e-commerce sales data, including:
- **Data Generation**: Creates realistic sample e-commerce datasets
- **Data Cleaning**: Handles duplicates, missing values, and data type conversions
- **Sales Analysis**: Calculates key metrics, trends, and insights
- **Power BI Ready**: Exports cleaned data and analysis results in CSV format

## 🎯 Features

- **1000+ Sample Records**: Realistic e-commerce data with multiple categories
- **Comprehensive Data Cleaning**: Removes duplicates, handles missing values, validates data
- **Derived Metrics**: Total Sales, Profit Margin, Profit calculations
- **Sales Analytics**: 
  - Total Sales and Revenue
  - Best-selling products (top 10)
  - High-revenue categories
  - Monthly/Quarterly sales trends
  - Average Order Value (AOV)
  - Regional analysis

## 📁 Project Structure

```
Business Sales Dashboard/
│
├── data_generator.py          # Generates sample e-commerce dataset
├── data_cleaner.py            # Cleans and preprocesses data
├── analysis.py                # Performs sales analysis and calculations
├── README.md                  # Project documentation
│
├── raw_ecommerce_data.csv     # Generated raw data (created after running generator)
├── cleaned_ecommerce_data.csv # Cleaned data ready for Power BI (created after cleaning)
│
└── analysis_output/           # Analysis results (created after running analysis)
    ├── top_products_by_quantity.csv
    ├── top_products_by_revenue.csv
    ├── category_analysis.csv
    ├── monthly_trends.csv
    ├── quarterly_trends.csv
    ├── regional_analysis.csv
    ├── aov_by_category.csv
    └── aov_by_region.csv
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Required Python libraries:
  - pandas
  - numpy

### Installation

1. **Clone or download this project** to your local machine

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install pandas numpy
   ```

## 📊 Usage Guide

### Step 1: Generate Sample Data

Run the data generator to create a sample e-commerce dataset:

```bash
python data_generator.py
```

This will create `raw_ecommerce_data.csv` with 1000+ records containing:
- OrderID, ProductID, ProductName, Category
- Quantity, Price, Revenue
- OrderDate, CustomerID, Region

**Output**: `raw_ecommerce_data.csv`

### Step 2: Clean the Data

Run the data cleaning script to preprocess the data:

```bash
python data_cleaner.py
```

This script will:
- Remove duplicate records
- Handle missing values (fills with appropriate defaults)
- Convert data types correctly
- Create derived columns (TotalSales, ProfitMargin, Profit, date components)
- Remove outliers and invalid data

**Output**: `cleaned_ecommerce_data.csv` (ready for Power BI import)

### Step 3: Run Analysis

Execute the analysis script to generate insights:

```bash
python analysis.py
```

This will:
- Calculate total sales and revenue metrics
- Identify best-selling products
- Analyze high-revenue categories
- Generate monthly/quarterly sales trends
- Calculate average order value
- Perform regional analysis
- Export all results to CSV files

**Output**: Multiple CSV files in `analysis_output/` directory

## 📈 Data Schema

### Input Data Columns

| Column | Type | Description |
|--------|------|-------------|
| OrderID | String | Unique order identifier |
| ProductID | String | Unique product identifier |
| ProductName | String | Name of the product |
| Category | String | Product category |
| Quantity | Integer | Number of items ordered |
| Price | Float | Unit price of product |
| Revenue | Float | Total revenue (Price × Quantity) |
| OrderDate | DateTime | Date of the order |
| CustomerID | String | Unique customer identifier |
| Region | String | Sales region |

### Derived Columns (After Cleaning)

| Column | Type | Description |
|--------|------|-------------|
| TotalSales | Float | Total sales amount (same as Revenue) |
| ProfitMargin | Float | Profit margin percentage by category |
| Profit | Float | Calculated profit (Revenue × ProfitMargin) |
| Year | Integer | Year extracted from OrderDate |
| Month | Integer | Month extracted from OrderDate |
| Quarter | Integer | Quarter extracted from OrderDate |
| MonthName | String | Month name (e.g., "January") |
| YearMonth | String | Year-Month format (e.g., "2024-01") |
| DaysSinceOrder | Integer | Days since order date |

## 🔍 Key Insights Generated

### 1. Total Sales Metrics
- Total Revenue
- Total Sales
- Total Profit
- Total Orders
- Total Products Sold
- Average Order Value (AOV)

### 2. Best-Selling Products
- Top 10 products by quantity sold
- Top 10 products by revenue generated

### 3. Category Analysis
- Revenue by category
- Quantity sold by category
- Order count by category
- Profit by category
- Revenue percentage distribution

### 4. Sales Trends
- Monthly sales trends (revenue, quantity, orders)
- Quarterly sales trends
- Time-based performance analysis

### 5. Average Order Value
- Overall AOV
- AOV by category
- AOV by region

### 6. Regional Analysis
- Revenue by region
- Customer count by region
- Order distribution by region

## 📊 Power BI Integration

### Importing Data into Power BI

1. **Open Power BI Desktop**

2. **Import the cleaned dataset**:
   - Click "Get Data" → "Text/CSV"
   - Select `cleaned_ecommerce_data.csv`
   - Click "Load"

3. **Import analysis results** (optional):
   - Import additional CSV files from `analysis_output/` folder
   - These provide pre-calculated metrics for faster dashboard creation

### Recommended Power BI Visualizations

- **Sales Overview**: Cards showing Total Revenue, Total Orders, AOV
- **Product Performance**: Bar/Column charts for top products
- **Category Analysis**: Pie/Donut chart for revenue by category
- **Sales Trends**: Line chart for monthly/quarterly trends
- **Regional Map**: Map visualization showing sales by region
- **Time Series**: Date slicer with trend analysis

## 🛠️ Customization

### Adjusting Data Generation

Edit `data_generator.py` to:
- Change number of records: Modify `num_records` parameter
- Add/remove categories: Update `categories` list
- Modify product names: Update `products` dictionary
- Adjust price ranges: Modify `base_prices` dictionary

### Modifying Cleaning Logic

Edit `data_cleaner.py` to:
- Change missing value handling strategies
- Adjust outlier detection thresholds
- Add custom validation rules
- Create additional derived columns

### Extending Analysis

Edit `analysis.py` to:
- Add new metrics and calculations
- Create custom analysis functions
- Export additional analysis results
- Integrate with other data sources

## 📝 Notes

- **Random Seed**: The data generator uses a fixed random seed (42) for reproducibility
- **Profit Margins**: Assumed profit margins range from 20-40% based on category
- **Date Range**: Generated data spans the last 2 years from the current date
- **Missing Values**: Approximately 5% of records have missing values for testing cleaning logic
- **Duplicates**: Approximately 2% duplicate records are introduced for testing deduplication

## 🔧 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure pandas and numpy are installed
   ```bash
   pip install pandas numpy
   ```

2. **FileNotFoundError**: Run scripts in order (generator → cleaner → analysis)

3. **Memory Issues**: Reduce `num_records` in data_generator.py if working with limited memory

## 📄 License

This project is provided as-is for educational and business analysis purposes.

## 👤 Author

Created for Business Sales Dashboard project

## 📅 Last Updated

2025

---

**Happy Analyzing! 📊**

