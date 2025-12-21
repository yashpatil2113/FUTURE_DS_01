"""
Generate HTML Dashboard for E-commerce Sales Analysis
Creates a beautiful, interactive dashboard with classic sigma theme
"""

import pandas as pd
import json
from datetime import datetime

def load_analysis_data():
    """Load all analysis data files"""
    data = {}
    
    # Load cleaned data for summary metrics
    df = pd.read_csv('cleaned_ecommerce_data.csv')
    
    # Calculate summary metrics
    data['total_revenue'] = df['Revenue'].sum()
    data['total_profit'] = df['Profit'].sum()
    data['total_orders'] = df['OrderID'].nunique()
    data['total_products_sold'] = df['Quantity'].sum()
    data['total_customers'] = df['CustomerID'].nunique()
    data['avg_order_value'] = data['total_revenue'] / data['total_orders']
    
    # Load analysis outputs
    data['category_analysis'] = pd.read_csv('analysis_output/category_analysis.csv')
    data['monthly_trends'] = pd.read_csv('analysis_output/monthly_trends.csv')
    data['quarterly_trends'] = pd.read_csv('analysis_output/quarterly_trends.csv')
    data['top_products'] = pd.read_csv('analysis_output/top_products_by_revenue.csv')
    data['regional_analysis'] = pd.read_csv('analysis_output/regional_analysis.csv')
    data['aov_by_category'] = pd.read_csv('analysis_output/aov_by_category.csv')
    data['aov_by_region'] = pd.read_csv('analysis_output/aov_by_region.csv')
    
    return data

def generate_html_dashboard():
    """Generate the HTML dashboard"""
    data = load_analysis_data()
    
    # Prepare chart data
    # Category revenue data
    categories = data['category_analysis']['Category'].tolist()
    category_revenue = data['category_analysis']['TotalRevenue'].tolist()
    category_profit = data['category_analysis']['TotalProfit'].tolist()
    
    # Monthly trends data
    monthly_labels = data['monthly_trends']['YearMonth'].tolist()
    monthly_revenue = data['monthly_trends']['TotalRevenue'].tolist()
    monthly_orders = data['monthly_trends']['OrderCount'].tolist()
    
    # Quarterly trends data
    quarterly_labels = data['quarterly_trends']['YearQuarter'].tolist()
    quarterly_revenue = data['quarterly_trends']['TotalRevenue'].tolist()
    
    # Regional data
    regions = data['regional_analysis']['Region'].tolist()
    regional_revenue = data['regional_analysis']['TotalRevenue'].tolist()
    
    # Top products data
    top_products = data['top_products'].head(10)
    
    # AOV by category
    aov_categories = data['aov_by_category']['Category'].tolist()
    aov_values = data['aov_by_category']['AverageOrderValue'].tolist()
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Sales Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body class="bg-slate-100 text-slate-900">
    <div class="max-w-7xl mx-auto px-6 py-8">
        <header class="mb-8 border-b border-slate-200 pb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
                <h1 class="text-2xl font-semibold text-slate-900">Business Sales Dashboard</h1>
                <p class="mt-1 text-sm text-slate-500">E-commerce performance overview</p>
            </div>
            <p class="text-xs text-slate-400">
                Last updated {datetime.now().strftime('%B %d, %Y %H:%M')}
            </p>
        </header>

        <section aria-label="Key metrics" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <p class="text-xs font-medium text-slate-500 uppercase tracking-wide">Total Revenue</p>
                <p class="mt-2 text-2xl font-semibold text-slate-900">${data['total_revenue']:,.2f}</p>
            </div>
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <p class="text-xs font-medium text-slate-500 uppercase tracking-wide">Total Profit</p>
                <p class="mt-2 text-2xl font-semibold text-slate-900">${data['total_profit']:,.2f}</p>
                <p class="mt-1 text-xs text-slate-500">{data['total_profit']/data['total_revenue']*100:.1f}% margin</p>
            </div>
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <p class="text-xs font-medium text-slate-500 uppercase tracking-wide">Total Orders</p>
                <p class="mt-2 text-2xl font-semibold text-slate-900">{data['total_orders']:,}</p>
            </div>
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <p class="text-xs font-medium text-slate-500 uppercase tracking-wide">Average Order Value</p>
                <p class="mt-2 text-2xl font-semibold text-slate-900">${data['avg_order_value']:,.2f}</p>
            </div>
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <p class="text-xs font-medium text-slate-500 uppercase tracking-wide">Products Sold</p>
                <p class="mt-2 text-2xl font-semibold text-slate-900">{data['total_products_sold']:,}</p>
            </div>
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <p class="text-xs font-medium text-slate-500 uppercase tracking-wide">Unique Customers</p>
                <p class="mt-2 text-2xl font-semibold text-slate-900">{data['total_customers']:,}</p>
            </div>
        </section>

        <section aria-label="Charts" class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <h2 class="text-sm font-medium text-slate-700 mb-3">Revenue by Category</h2>
                <div class="h-64">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <h2 class="text-sm font-medium text-slate-700 mb-3">Monthly Sales Trend</h2>
                <div class="h-64">
                    <canvas id="monthlyChart"></canvas>
                </div>
            </div>
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <h2 class="text-sm font-medium text-slate-700 mb-3">Quarterly Revenue</h2>
                <div class="h-64">
                    <canvas id="quarterlyChart"></canvas>
                </div>
            </div>
            <div class="bg-slate-50 border border-slate-200 rounded-lg p-4 shadow-sm">
                <div class="flex items-start justify-between gap-4 mb-3">
                    <div>
                        <h2 class="text-sm font-medium text-slate-800">Revenue by Region</h2>
                        <p class="mt-1 text-xs text-slate-500">How total revenue is distributed across regions.</p>
                    </div>
                    <span class="inline-flex items-center rounded-full border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-medium text-slate-500">
                        Share by region
                    </span>
                </div>
                <div class="h-64">
                    <canvas id="regionalChart"></canvas>
                </div>
            </div>
            <div class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
                <h2 class="text-sm font-medium text-slate-700 mb-3">Average Order Value by Category</h2>
                <div class="h-64">
                    <canvas id="aovChart"></canvas>
                </div>
            </div>
            <div class="bg-slate-50 border border-slate-200 rounded-lg p-4 shadow-sm">
                <div class="flex items-start justify-between gap-4 mb-3">
                    <div>
                        <h2 class="text-sm font-medium text-slate-800">Profit by Category</h2>
                        <p class="mt-1 text-xs text-slate-500">Relative contribution of each product category to total profit.</p>
                    </div>
                    <span class="inline-flex items-center rounded-full border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-medium text-slate-500">
                        Percent of total
                    </span>
                </div>
                <div class="h-64">
                    <canvas id="profitChart"></canvas>
                </div>
            </div>
        </section>

        <section aria-label="Top products" class="bg-white border border-slate-200 rounded-lg p-4 shadow-sm mb-8">
            <h2 class="text-sm font-medium text-slate-700 mb-3">Top 10 Products by Revenue</h2>
            <div class="overflow-x-auto">
                <table class="min-w-full text-sm text-left">
                    <thead class="border-b border-slate-200 bg-slate-50 text-xs font-medium text-slate-500 uppercase tracking-wide">
                        <tr>
                            <th scope="col" class="px-3 py-2">Rank</th>
                            <th scope="col" class="px-3 py-2">Product</th>
                            <th scope="col" class="px-3 py-2">Category</th>
                            <th scope="col" class="px-3 py-2">Revenue</th>
                            <th scope="col" class="px-3 py-2">Quantity</th>
                            <th scope="col" class="px-3 py-2">Orders</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
"""
    
    # Add top products table rows
    for idx, row in top_products.iterrows():
        rank = idx + 1
        html_content += f"""
                    <tr>
                        <td>{rank}</td>
                        <td><strong>{row['ProductName']}</strong></td>
                        <td>{row['Category']}</td>
                        <td>${row['TotalRevenue']:,.2f}</td>
                        <td>{int(row['TotalQuantity'])}</td>
                        <td>{int(row['OrderCount'])}</td>
                    </tr>
"""
    
    html_content += """
                    </tbody>
                </table>
            </div>
        </section>

        <footer class="border-t border-slate-200 pt-4 text-xs text-slate-400">
            Business Sales Dashboard
        </footer>
    </div>

    <script>
        // Chart.js configuration
        Chart.defaults.color = '#0f172a';
        Chart.defaults.borderColor = '#e5e7eb';
        
        // Category Revenue Chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(categoryCtx, {
            type: 'bar',
            data: {
                labels: """ + json.dumps(categories) + """,
                datasets: [{
                    label: 'Revenue ($)',
                    data: """ + json.dumps(category_revenue) + """,
                    backgroundColor: 'rgba(74, 144, 226, 0.8)',
                    borderColor: 'rgba(74, 144, 226, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + context.parsed.y.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
        
        // Monthly Trends Chart
        const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
        new Chart(monthlyCtx, {
            type: 'line',
            data: {
                labels: """ + json.dumps(monthly_labels) + """,
                datasets: [{
                    label: 'Revenue',
                    data: """ + json.dumps(monthly_revenue) + """,
                    borderColor: 'rgba(74, 144, 226, 1)',
                    backgroundColor: 'rgba(74, 144, 226, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }, {
                    label: 'Orders',
                    data: """ + json.dumps(monthly_orders) + """,
                    borderColor: 'rgba(76, 175, 80, 1)',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                }
            }
        });
        
        // Quarterly Chart
        const quarterlyCtx = document.getElementById('quarterlyChart').getContext('2d');
        new Chart(quarterlyCtx, {
            type: 'bar',
            data: {
                labels: """ + json.dumps(quarterly_labels) + """,
                datasets: [{
                    label: 'Revenue ($)',
                    data: """ + json.dumps(quarterly_revenue) + """,
                    backgroundColor: 'rgba(156, 39, 176, 0.8)',
                    borderColor: 'rgba(156, 39, 176, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + context.parsed.y.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
        
        // Regional Chart
        const regionalCtx = document.getElementById('regionalChart').getContext('2d');
        new Chart(regionalCtx, {
            type: 'doughnut',
            data: {
                labels: """ + json.dumps(regions) + """,
                datasets: [{
                    data: """ + json.dumps(regional_revenue) + """,
                    backgroundColor: [
                        'rgba(74, 144, 226, 0.8)',
                        'rgba(156, 39, 176, 0.8)',
                        'rgba(76, 175, 80, 0.8)',
                        'rgba(255, 152, 0, 0.8)',
                        'rgba(244, 67, 54, 0.8)',
                        'rgba(33, 150, 243, 0.8)',
                        'rgba(158, 158, 158, 0.8)'
                    ],
                    borderColor: '#ffffff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '55%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 12,
                            boxHeight: 12,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return label + ': $' + value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
        
        // AOV by Category Chart
        const aovCtx = document.getElementById('aovChart').getContext('2d');
        new Chart(aovCtx, {
            type: 'bar',
            data: {
                labels: """ + json.dumps(aov_categories) + """,
                datasets: [{
                    label: 'AOV ($)',
                    data: """ + json.dumps(aov_values) + """,
                    backgroundColor: 'rgba(255, 152, 0, 0.8)',
                    borderColor: 'rgba(255, 152, 0, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + context.parsed.x.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
        
        // Profit by Category Chart
        const profitCtx = document.getElementById('profitChart').getContext('2d');
        new Chart(profitCtx, {
            type: 'doughnut',
            data: {
                labels: """ + json.dumps(categories) + """,
                datasets: [{
                    data: """ + json.dumps(category_profit) + """,
                    backgroundColor: [
                        'rgba(74, 144, 226, 0.8)',
                        'rgba(156, 39, 176, 0.8)',
                        'rgba(76, 175, 80, 0.8)',
                        'rgba(255, 152, 0, 0.8)',
                        'rgba(244, 67, 54, 0.8)',
                        'rgba(33, 150, 243, 0.8)',
                        'rgba(158, 158, 158, 0.8)',
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(0, 188, 212, 0.8)',
                        'rgba(139, 195, 74, 0.8)'
                    ],
                    borderColor: '#1a1a2e',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '55%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 12,
                            boxHeight: 12,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return label + ': $' + value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
"""
    
    return html_content

if __name__ == '__main__':
    print("Generating HTML dashboard...")
    html = generate_html_dashboard()
    
    output_file = 'dashboard.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Dashboard generated successfully!")
    print(f"Open '{output_file}' in your web browser to view the dashboard.")

