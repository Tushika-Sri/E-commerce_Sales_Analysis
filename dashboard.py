import streamlit as st
import pandas as pd

# Load data
# Load data with dtype specification or low_memory option
amazon_sales = pd.read_csv(
    'E-commerce_Sales_Analysis/Amazon Sale Report.csv',
    dtype={'Column23': str},  # Change 'Column23' to the actual name of the column
    low_memory=False  # Optional: can be used alone or with dtype
)
sales_report = pd.read_csv('E-commerce_Sales_Analysis/Sale Report.csv')
expense_data = pd.read_csv('E-commerce_Sales_Analysis/Expense IIGF.csv')

# Clean the data
sales_report.dropna(inplace=True)

# Check for 'Date' column and convert it if it exists
if 'Date' in sales_report.columns:
    sales_report['Date'] = pd.to_datetime(sales_report['Date'])
else:
    st.write("The 'Date' column is not found in the sales report.")

# Streamlit dashboard
st.title('E-Commerce Sales Performance Dashboard')

# Calculate total stock from the sales report
total_stock = sales_report['Stock'].sum()
st.write(f'Total Stock: {total_stock}')

# Calculate total sales from Amazon sales
if 'Amount' in amazon_sales.columns:
    total_amazon_sales = amazon_sales['Amount'].sum()
    st.write(f'Total Amazon Sales: ${total_amazon_sales:,.2f}')
else:
    st.write("The 'Amount' column is not found in the Amazon sales data.")

# Monthly Sales Trends (Using Stock since Qty does not exist)
monthly_sales = None
if 'Date' in sales_report.columns:
    sales_report['Month'] = sales_report['Date'].dt.to_period("M")
    monthly_sales = sales_report.groupby('Month')['Stock'].sum()  # Using Stock for visualization
    
    # Create a line chart for monthly stock trends
    st.subheader('Monthly Stock Trends')
    st.line_chart(monthly_sales)

# Show a dataframe of the sales report
st.subheader('Sales Report')
st.write(sales_report)

# Analyze and display profit margins
if 'Received Amount' in expense_data.columns and 'Gross Amount' in expense_data.columns:
    expense_data['Profit Margin'] = (expense_data['Received Amount'] - expense_data['Gross Amount']) / expense_data['Received Amount'] * 100
    st.subheader('Profit Margins')
    st.write(expense_data[['Received Amount', 'Gross Amount', 'Profit Margin']])

# Sales by Category
if 'Category' in sales_report.columns and 'Stock' in sales_report.columns:
    category_sales = sales_report.groupby('Category')['Stock'].sum().reset_index()  # Using Stock
    st.subheader('Sales by Category')
    st.bar_chart(category_sales.set_index('Category'))

# Top Selling Products by Stock
if 'SKU Code' in sales_report.columns:
    top_products = sales_report.groupby('SKU Code')['Stock'].sum().reset_index().sort_values(by='Stock', ascending=False).head(10)  # Using Stock
    st.subheader('Top Products by Stock')
    st.write(top_products)
else:
    st.write("The 'SKU Code' column is not found in the sales report.")

# Filters for Category, Size, and Color
st.sidebar.header('Filters')

# Unique categories for filter
if 'Category' in sales_report.columns:
    selected_category = st.sidebar.selectbox('Select Category:', ['All'] + sales_report['Category'].unique().tolist())
else:
    selected_category = 'All'

# Unique sizes for filter
if 'Size' in sales_report.columns:
    selected_size = st.sidebar.selectbox('Select Size:', ['All'] + sales_report['Size'].unique().tolist())
else:
    selected_size = 'All'

# Unique colors for filter
if 'Color' in sales_report.columns:
    selected_color = st.sidebar.selectbox('Select Color:', ['All'] + sales_report['Color'].unique().tolist())
else:
    selected_color = 'All'

# Filter the sales report based on selected filters
filtered_sales = sales_report.copy()

if selected_category != 'All':
    filtered_sales = filtered_sales[filtered_sales['Category'] == selected_category]

if selected_size != 'All':
    filtered_sales = filtered_sales[filtered_sales['Size'] == selected_size]

if selected_color != 'All':
    filtered_sales = filtered_sales[filtered_sales['Color'] == selected_color]

# Display filtered sales data
st.subheader('Filtered Sales Report')
st.write(filtered_sales)

# Visualize filtered sales by Category
if 'Category' in filtered_sales.columns and 'Stock' in filtered_sales.columns:
    category_filtered_sales = filtered_sales.groupby('Category')['Stock'].sum().reset_index()  # Using Stock
    st.subheader('Filtered Sales by Category')
    st.bar_chart(category_filtered_sales.set_index('Category'))

# Calculate and display Sales Growth Rate (only if monthly_sales is defined)
if monthly_sales is not None and len(monthly_sales) > 1:
    sales_growth = ((monthly_sales.iloc[-1] - monthly_sales.iloc[-2]) / monthly_sales.iloc[-2]) * 100
    st.write(f'Stock Growth Rate: {sales_growth:.2f}%')

# Display raw data for reference
st.subheader('Sales Report Data')
st.write(sales_report)
