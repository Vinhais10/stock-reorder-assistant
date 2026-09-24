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


def print_full_report(result):
    print("=" * 50)
    print("INVENTORY REORDER REPORT")
    print("=" * 50)
    for _, row in result.iterrows():
        status = "⚠️  REORDER NEEDED" if row['needs_reorder'] else "✅ OK"
        print(f"\n{row['product_name']} ({row['product_id']})")
        print(f"  Current stock: {row['current_stock']}")
        print(f"  Reorder point: {row['reorder_point']:.0f}")
        print(f"  Status: {status}")


def print_product_detail(result):
    product_id = input("Enter product ID (e.g. 85123A): ").strip()
    match = result[result['product_id'] == product_id]

    if match.empty:
        print(f"No product found with ID '{product_id}'.")
        return

    row = match.iloc[0]
    status = "⚠️  REORDER NEEDED" if row['needs_reorder'] else "✅ OK"
    print(f"\n{row['product_name']} ({row['product_id']})")
    print(f"  Average daily sales: {row['avg_daily_sales']:.1f}")
    print(f"  Current stock: {row['current_stock']}")
    print(f"  Reorder point: {row['reorder_point']:.0f}")
    print(f"  Status: {status}")


def show_menu():
    print("\n--- Stock Reorder Assistant ---")
    print("1. View full reorder report")
    print("2. View a specific product")
    print("3. Exit")


if __name__ == "__main__":
    sales = load_sales_data()
    products = pd.read_csv('products.csv')
    avg_daily_sales = calculate_avg_daily_sales(sales)
    result = calculate_reorder_points(products, avg_daily_sales)

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print_full_report(result)
        elif choice == "2":
            print_product_detail(result)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")