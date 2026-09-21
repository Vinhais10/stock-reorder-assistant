import pandas as pd

df = pd.read_excel('Online Retail.xlsx')

print(df.head())
print()
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print()
print(df.columns.tolist())
top_products = df.groupby('StockCode')['Quantity'].sum().sort_values(ascending=False)
print(top_products.head(10))
top_10_codes = top_products.head(10).index.tolist()
names = df[df['StockCode'].isin(top_10_codes)][['StockCode', 'Description']].drop_duplicates()
print(names)