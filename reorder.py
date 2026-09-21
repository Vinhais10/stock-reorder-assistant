import pandas as pd

TARGET_PRODUCTS = ['85123A', '84879', '21212', '22616']


def load_sales_data():
    df = pd.read_excel('Online Retail.xlsx')
    df['StockCode'] = df['StockCode'].astype(str)
    df = df[df['StockCode'].isin(TARGET_PRODUCTS)]
    df = df.dropna(subset=['Quantity', 'InvoiceDate'])
    df = df[df['Quantity'] > 0]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df


def calculate_avg_daily_sales(df):
    total_sold = df.groupby('StockCode')['Quantity'].sum()
    num_days = (df['InvoiceDate'].max() - df['InvoiceDate'].min()).days + 1
    avg_daily_sales = total_sold / num_days
    return avg_daily_sales.reset_index(name='avg_daily_sales').rename(columns={'StockCode': 'product_id'})


def calculate_reorder_points(products, avg_daily_sales):
    result = products.merge(avg_daily_sales, on='product_id')
    result['reorder_point'] = (result['avg_daily_sales'] * result['lead_time_days']) + result['safety_stock']
    result['needs_reorder'] = result['current_stock'] < result['reorder_point']
    return result


if __name__ == "__main__":
    sales = load_sales_data()
    products = pd.read_csv('products.csv')

    avg_daily_sales = calculate_avg_daily_sales(sales)
    result = calculate_reorder_points(products, avg_daily_sales)

    print(result[['product_id', 'product_name', 'current_stock', 'reorder_point', 'needs_reorder']])