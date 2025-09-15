# Comprehensive Guide to Data Cleaning with Pandas

import pandas as pd
import numpy as np
from datetime import datetime

"""
PART 1: BASIC PANDAS CONCEPTS
----------------------------
Before we dive into data cleaning, let's understand the fundamental building blocks of pandas.
"""

# Creating a DataFrame
# DataFrames are 2-dimensional labeled data structures
df = pd.DataFrame({
    'product': ['Laptop', 'Phone', 'Tablet', 'Watch'],
    'price': ['$999.99', '$599.99', '$299.99', '$199.99'],
    'stock': [10, 15, None, 20],
    'rating': [4.5, 4.8, 4.2, '4.6'],
    'date_added': ['2024-01-01', '2024-01-02', '2024/01/03', '01-04-2024']
})

"""
PART 2: INITIAL DATA INSPECTION
------------------------------
Always start by examining your data to understand its structure and potential issues.
"""

# Basic inspection methods
df.head()        # View first 5 rows
df.info()        # Get data types and non-null counts
df.describe()    # Statistical summary of numerical columns
df.dtypes        # Data types of each column
df.isnull().sum()  # Count of null values in each column

"""
PART 3: COMMON DATA CLEANING OPERATIONS
-------------------------------------
Let's cover the most frequent cleaning operations you'll need for scraped data.
"""

# 1. Handling Missing Values
def clean_missing_values(df):
    # Fill missing values based on data type
    df['stock'] = df['stock'].fillna(df['stock'].mean())  # Fill with mean for numerical
    df['product'] = df['product'].fillna('Unknown')  # Fill with string for categorical
    
    # Alternative: Drop rows with missing values
    df_cleaned = df.dropna(subset=['critical_column'])  # Only drop if specific columns are null
    
    return df

# 2. Standardizing Data Types
def standardize_types(df):
    # Convert price from string to float
    df['price'] = df['price'].str.replace('$', '').astype(float)
    
    # Convert rating to float (handling mixed types)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    
    # Standardize dates
    df['date_added'] = pd.to_datetime(df['date_added'])
    
    return df

# 3. Cleaning Text Data
def clean_text(df):
    # Remove leading/trailing whitespace
    df['product'] = df['product'].str.strip()
    
    # Convert to lowercase
    df['product'] = df['product'].str.lower()
    
    # Remove special characters
    df['product'] = df['product'].str.replace('[^\w\s]', '')
    
    return df

"""
PART 4: ADVANCED CLEANING TECHNIQUES
----------------------------------
More sophisticated cleaning operations for complex datasets.
"""

# 1. Handling Duplicates
def handle_duplicates(df):
    # Identify duplicates
    duplicates = df.duplicated().sum()
    
    # Remove exact duplicates
    df = df.drop_duplicates()
    
    # Remove duplicates based on specific columns
    df = df.drop_duplicates(subset=['product', 'price'], keep='first')
    
    return df

# 2. Outlier Detection and Handling
def handle_outliers(df, column, method='iqr'):
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Replace outliers with bounds
        df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
    
    elif method == 'zscore':
        z_scores = abs((df[column] - df[column].mean()) / df[column].std())
        df[column] = df[column].mask(z_scores > 3, df[column].mean())
    
    return df

# 3. Category Standardization
def standardize_categories(df, column):
    # Create mapping for similar categories
    category_mapping = {
        'laptop': 'Laptop',
        'notebooks': 'Laptop',
        'smart phone': 'Phone',
        'mobile': 'Phone',
        'smart watch': 'Watch',
        'wearable': 'Watch'
    }
    
    df[column] = df[column].map(category_mapping).fillna(df[column])
    return df

"""
PART 5: PRACTICAL EXAMPLE - CLEANING SCRAPED E-COMMERCE DATA
---------------------------------------------------------
Let's put it all together with a real-world example.
"""

def clean_ecommerce_data(df):
    # Make a copy to avoid modifying original data
    df_cleaned = df.copy()
    
    # 1. Initial cleaning
    df_cleaned = clean_missing_values(df_cleaned)
    df_cleaned = standardize_types(df_cleaned)
    df_cleaned = clean_text(df_cleaned)
    
    # 2. Handle duplicates
    df_cleaned = handle_duplicates(df_cleaned)
    
    # 3. Clean numerical columns
    numeric_columns = ['price', 'rating']
    for col in numeric_columns:
        df_cleaned = handle_outliers(df_cleaned, col)
    
    # 4. Standardize categories
    df_cleaned = standardize_categories(df_cleaned, 'product')
    
    # 5. Create derived features
    df_cleaned['price_category'] = pd.qcut(df_cleaned['price'], 
                                         q=4, 
                                         labels=['Budget', 'Economy', 'Premium', 'Luxury'])
    
    # 6. Final validation
    assert df_cleaned.isnull().sum().sum() == 0, "There are still null values in the dataset"
    assert df_cleaned.duplicated().sum() == 0, "There are still duplicates in the dataset"
    
    return df_cleaned

"""
PART 6: EXAMPLE USAGE WITH SCRAPED DATA
-------------------------------------
Here's how to use these functions with real scraped data.
"""

# Example of cleaning scraped product data
scraped_data = pd.DataFrame({
    'product_name': ['  laptop Pro 13"  ', 'Smart phone X', 'tablet air', None],
    'product_price': ['$1,299.99', '$899.99', 'Contact Us', '$499.99'],
    'rating_count': ['1,234', '956', '476', ''],
    'avg_rating': [4.7, 3.9, None, 4.2],
    'last_updated': ['2024-01-01', '01/02/2024', '2024.01.03', '01-04-2024']
})

def clean_scraped_products(df):
    # Clean product names
    df['product_name'] = df['product_name'].fillna('Unknown Product')
    df['product_name'] = df['product_name'].str.strip().str.lower()
    
    # Clean prices
    df['product_price'] = df['product_price'].replace('Contact Us', np.nan)
    df['product_price'] = df['product_price'].str.replace('[$,]', '', regex=True)
    df['product_price'] = pd.to_numeric(df['product_price'], errors='coerce')
    
    # Clean ratings
    df['rating_count'] = df['rating_count'].str.replace(',', '').replace('', '0')
    df['rating_count'] = pd.to_numeric(df['rating_count'])
    df['avg_rating'] = df['avg_rating'].fillna(df['avg_rating'].mean())
    
    # Standardize dates
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    
    return df

# Example usage
cleaned_df = clean_scraped_products(scraped_data)

"""
PART 7: BEST PRACTICES AND TIPS
------------------------------
1. Always make a copy of your original data before cleaning
2. Document your cleaning steps and assumptions
3. Validate your data after each major transformation
4. Create reusable cleaning functions for similar datasets
5. Keep track of how many rows/columns are modified in each step
6. Use appropriate data types to save memory
7. Handle errors gracefully with try-except blocks
8. Create automated tests for your cleaning functions
"""

# Example of a data cleaning pipeline with logging
def clean_data_with_logging(df):
    original_shape = df.shape
    modifications = {}
    
    # Copy original data
    df_cleaned = df.copy()
    
    # Track missing values
    initial_nulls = df_cleaned.isnull().sum().sum()
    df_cleaned = clean_missing_values(df_cleaned)
    final_nulls = df_cleaned.isnull().sum().sum()
    modifications['nulls_filled'] = initial_nulls - final_nulls
    
    # Track duplicates removed
    initial_dupes = df_cleaned.duplicated().sum()
    df_cleaned = handle_duplicates(df_cleaned)
    final_dupes = df_cleaned.duplicated().sum()
    modifications['duplicates_removed'] = initial_dupes - final_dupes
    
    # Track outliers handled
    numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
    outliers_modified = 0
    for col in numeric_cols:
        original_outliers = len(df_cleaned[abs(df_cleaned[col] - df_cleaned[col].mean()) > 
                                         (3 * df_cleaned[col].std())])
        df_cleaned = handle_outliers(df_cleaned, col)
        new_outliers = len(df_cleaned[abs(df_cleaned[col] - df_cleaned[col].mean()) > 
                                    (3 * df_cleaned[col].std())])
        outliers_modified += original_outliers - new_outliers
    modifications['outliers_handled'] = outliers_modified
    
    final_shape = df_cleaned.shape
    modifications['rows_removed'] = original_shape[0] - final_shape[0]
    
    return df_cleaned, modifications

"""
PART 8: WORKING WITH CSV FILES - PRACTICAL EXAMPLE
------------------------------------------------
Let's work through a complete example of reading and cleaning a CSV file,
dealing with common real-world issues you might encounter.
"""

# Example CSV data structure:
'''
date,customer_id,product_name,quantity,price,payment_method,shipping_address
2024-01-15,CS123,Premium Laptop,1,"1,499.99",credit card,"123 Main St, Austin, TX 78701"
2024/01/16,CS124,wireless mouse,,24.99,PayPal,"456 Oak Ave, Seattle WA 98101"
1/17/24,CS123,Premium laptop,2,"1499.99",Credit Card,"123 Main St, Austin TX 78701"
2024-01-17,CS125,Gaming Monitor,1,null,debit card,"789 Pine Rd Seattle, WA 98101"
'''

def read_and_clean_sales_data(file_path):
    """
    Read and clean a sales data CSV file, handling common issues like:
    - Inconsistent date formats
    - Different price formats and currency symbols
    - Missing values
    - Duplicate entries
    - Inconsistent text formatting
    - Address standardization
    
    Parameters:
    file_path (str): Path to the CSV file
    
    Returns:
    pd.DataFrame: Cleaned DataFrame
    dict: Summary of cleaning operations performed
    """
    # Initialize tracking dictionary for cleaning operations
    cleaning_summary = {
        'original_rows': 0,
        'final_rows': 0,
        'missing_values_filled': 0,
        'duplicates_removed': 0,
        'date_format_fixes': 0,
        'price_format_fixes': 0
    }
    
    # Read the CSV file with common options
    df = pd.read_csv(
        file_path,
        # Handle missing values more flexibly
        na_values=['null', 'NULL', 'N/A', '', 'NaN'],
        # Handle potential encoding issues
        encoding='utf-8',
        # Handle potential quoting issues in fields
        quoting=csv.QUOTE_MINIMAL,
        # Skip bad lines but log them
        on_bad_lines='warn'
    )
    
    cleaning_summary['original_rows'] = len(df)
    
    # 1. Clean and standardize dates
    def standardize_date(date_str):
        try:
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%m/%d/%y']:
                try:
                    return pd.to_datetime(date_str, format=fmt)
                except:
                    continue
            # If none of the specific formats work, let pandas try to figure it out
            return pd.to_datetime(date_str)
        except:
            return pd.NaT
    
    original_invalid_dates = df['date'].isna().sum()
    df['date'] = df['date'].apply(standardize_date)
    cleaning_summary['date_format_fixes'] = original_invalid_dates - df['date'].isna().sum()
    
    # 2. Clean and standardize prices
    def clean_price(price):
        if pd.isna(price):
            return np.nan
        if isinstance(price, (int, float)):
            return float(price)
        # Remove currency symbols and commas, then convert to float
        price_str = str(price).replace('$', '').replace(',', '')
        try:
            return float(price_str)
        except:
            return np.nan
    
    original_invalid_prices = df['price'].isna().sum()
    df['price'] = df['price'].apply(clean_price)
    cleaning_summary['price_format_fixes'] = original_invalid_prices - df['price'].isna().sum()
    
    # 3. Standardize product names
    df['product_name'] = df['product_name'].str.strip().str.title()
    
    # 4. Clean and standardize payment methods
    payment_method_mapping = {
        'credit card': 'Credit Card',
        'credit': 'Credit Card',
        'debit card': 'Debit Card',
        'debit': 'Debit Card',
        'paypal': 'PayPal'
    }
    df['payment_method'] = df['payment_method'].str.lower().map(payment_method_mapping)
    
    # 5. Standardize shipping addresses
    def standardize_address(address):
        if pd.isna(address):
            return address
        
        # Remove extra spaces
        address = ' '.join(address.split())
        
        # Standardize state abbreviations
        state_pattern = r'([A-Za-z]+)\s*,?\s*([A-Z]{2})\s*(\d{5})?'
        match = re.search(state_pattern, address)
        if match:
            city, state, zip_code = match.groups()
            zip_code = zip_code if zip_code else ''
            standardized_end = f"{city}, {state} {zip_code}".strip()
            address = re.sub(state_pattern, standardized_end, address)
        
        return address
    
    df['shipping_address'] = df['shipping_address'].apply(standardize_address)
    
    # 6. Handle missing values
    original_nulls = df.isnull().sum().sum()
    
    # Fill missing quantities with 1 (assuming single item orders)
    df['quantity'] = df['quantity'].fillna(1)
    
    # Fill other missing values appropriately
    df['payment_method'] = df['payment_method'].fillna('Unknown')
    
    cleaning_summary['missing_values_filled'] = original_nulls - df.isnull().sum().sum()
    
    # 7. Remove duplicates
    original_dupes = df.duplicated().sum()
    df = df.drop_duplicates(subset=['date', 'customer_id', 'product_name', 'quantity'], 
                          keep='first')
    cleaning_summary['duplicates_removed'] = original_dupes
    
    # 8. Add derived columns
    df['total_amount'] = df['quantity'] * df['price']
    df['order_month'] = df['date'].dt.to_period('M')
    
    # 9. Final validation
    # Ensure all critical columns have appropriate data types
    assert df['date'].dtype == 'datetime64[ns]'
    assert df['price'].dtype == 'float64'
    assert df['quantity'].dtype == 'float64'
    
    cleaning_summary['final_rows'] = len(df)
    
    return df, cleaning_summary

# Example usage:
if __name__ == "__main__":
    # Read and clean the data
    df, summary = read_and_clean_sales_data('sales_data.csv')
    
    # Print cleaning summary
    print("\nData Cleaning Summary:")
    print(f"Original rows: {summary['original_rows']}")
    print(f"Final rows: {summary['final_rows']}")
    print(f"Missing values filled: {summary['missing_values_filled']}")
    print(f"Duplicates removed: {summary['duplicates_removed']}")
    print(f"Date format fixes: {summary['date_format_fixes']}")
    print(f"Price format fixes: {summary['price_format_fixes']}")
    
    # Basic data quality checks
    print("\nData Quality Report:")
    print(f"Null values remaining: {df.isnull().sum().sum()}")
    print(f"Duplicate rows remaining: {df.duplicated().sum()}")
    print("\nColumn Data Types:")
    print(df.dtypes)
    
    # Generate some basic insights
    print("\nBasic Analysis:")
    print("\nSales by Payment Method:")
    print(df.groupby('payment_method')['total_amount'].agg(['count', 'sum']))
    
    print("\nTop 5 Products by Revenue:")
    print(df.groupby('product_name')['total_amount'].sum().sort_values(ascending=False).head())
    
    # Example of saving the cleaned data
    df.to_csv('cleaned_sales_data.csv', index=False)