import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load all the datasets
sale_report = pd.read_csv('E-commerce_Sales_Analysis/Sale Report.csv')
amazon_sale_report = pd.read_csv('E-commerce_Sales_Analysis/Amazon Sale Report.csv')
cloud_warehouse = pd.read_csv('E-commerce_Sales_Analysis/Cloud Warehouse Compersion Chart.csv')
pl_march_2021 = pd.read_csv('E-commerce_Sales_Analysis/PLMarch 2021.csv')
may_2022 = pd.read_csv('E-commerce_Sales_Analysis/May-2022.csv')
international_sale_report = pd.read_csv('E-commerce_Sales_Analysis/International sale Report.csv')
expense_iigf = pd.read_csv('E-commerce_Sales_Analysis/Expense IIGF.csv')


# Cleaning and standardizing column names
def clean_columns(df):
    df.columns = df.columns.str.strip().str.upper()
    return df

sale_report = clean_columns(sale_report)
amazon_sale_report = clean_columns(amazon_sale_report)
cloud_warehouse = clean_columns(cloud_warehouse)
pl_march_2021 = clean_columns(pl_march_2021)
may_2022 = clean_columns(may_2022)
international_sale_report = clean_columns(international_sale_report)
expense_iigf = clean_columns(expense_iigf)

# Clean and standardize column names
sale_report.columns = sale_report.columns.str.strip().str.upper()

# Check for missing values
missing_values = sale_report.isnull().sum()
print(missing_values)

# Filling missing values without using inplace=True
sale_report['SKU CODE'] = sale_report['SKU CODE'].fillna('Unknown')
sale_report['DESIGN NO.'] = sale_report['DESIGN NO.'].fillna('Unknown')
sale_report['CATEGORY'] = sale_report['CATEGORY'].fillna('Unknown')
sale_report['SIZE'] = sale_report['SIZE'].fillna('Unknown')
sale_report['COLOR'] = sale_report['COLOR'].fillna('Unknown')
sale_report['STOCK'] = sale_report['STOCK'].fillna(0) 


# Re-check for missing values after handling
missing_values_after = sale_report.isnull().sum()
print(missing_values_after)

# Step 5: Merge Datasets
# Merge Sale Report with International Sale Report on SKU
merged_data = pd.merge(sale_report, international_sale_report, left_on='SKU CODE', right_on='SKU', how='left')

# Step 6: Calculate Total Sales and Profitability
# Total sales from Amazon Sale Report
total_amazon_sales = amazon_sale_report['AMOUNT'].sum()
print(f'Total Amazon Sales: ${total_amazon_sales:,.2f}')

# Ensure the columns are numeric
cloud_warehouse['SHIPROCKET'] = pd.to_numeric(cloud_warehouse['SHIPROCKET'], errors='coerce')
cloud_warehouse['INCREFF'] = pd.to_numeric(cloud_warehouse['INCREFF'], errors='coerce')

# Now, you can safely sum the columns
cloud_profit = cloud_warehouse['SHIPROCKET'].sum() + cloud_warehouse['INCREFF'].sum()
print(f'Total Profit from Cloud Warehouse: ${cloud_profit:,.2f}')

# Step 7: Analyze Price Competitiveness
price_columns = ['TP 1', 'TP 2', 'AJIO MRP', 'AMAZON MRP', 'FLIPKART MRP']


print(pl_march_2021[price_columns].dtypes)
print(pl_march_2021[price_columns].head())

for col in price_columns:
    pl_march_2021[col] = pl_march_2021[col].str.strip()  # Remove leading/trailing spaces if any
for col in price_columns:
    pl_march_2021[col] = pd.to_numeric(pl_march_2021[col], errors='coerce')  # Convert to numeric, coercing errors to NaN
print(pl_march_2021[price_columns].dtypes)

plt.figure(figsize=(12, 6))
sns.boxplot(data=pl_march_2021[price_columns])
plt.title("Price Distribution")
plt.xticks(rotation=45)
plt.show()

# Calculate mean of the price columns
price_analysis = pl_march_2021[price_columns].mean()
print(price_analysis)  # Display the mean values

# Export the cleaned DataFrame to a CSV file
pl_march_2021.to_csv('cleaned_data.csv', index=False)
