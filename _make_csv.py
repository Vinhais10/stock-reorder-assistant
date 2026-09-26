import pandas as pd
from reorder import load_sales_data
df = load_sales_data()
print("Linhas:", len(df))
print("Produtos:", df["StockCode"].unique())
df.to_csv("sales_data_filtered.csv", index=False)
print("Criado: sales_data_filtered.csv")
