\# Stock Reorder Assistant



A Python tool that calculates inventory reorder points using real retail transaction data, flagging products that need restocking based on historical demand, supplier lead time, and safety stock.



!\[Python](https://img.shields.io/badge/python-3.14-blue.svg)

!\[Status](https://img.shields.io/badge/status-active-brightgreen.svg)



\## Features



\- Loads and cleans real transaction data (541,909 rows from the UCI "Online Retail" dataset)

\- Calculates average daily demand per product from historical sales

\- Computes the reorder point using the formula: `(avg daily sales × lead time) + safety stock`

\- Flags products below their reorder point with a clear, readable report

\- Unit tested with synthetic data to validate the calculation logic



\## Data Source



Sales data comes from the \[UCI Machine Learning Repository's "Online Retail" dataset](https://archive.ics.uci.edu/dataset/352/online+retail) — real transactions from a UK-based online retailer (2010–2011), anonymized for research use. Lead time and safety stock values are illustrative business parameters, since the original dataset doesn't include supplier information.



\## Tech Stack



\- \*\*Python 3.14\*\*

\- \*\*pandas\*\* — data loading, cleaning, and aggregation



\## Setup



1\. Clone this repository

2\. Install dependencies: `pip install pandas openpyxl`

3\. Download the dataset from UCI and place `Online Retail.xlsx` in the project folder

4\. Run: `py reorder.py`



\## How It Works



`reorder.py` loads the raw Excel file, filters it down to a set of target products, and cleans it (removes missing values and returns/negative quantities). It calculates each product's average daily sales over the full history, then applies the reorder point formula per product using data from `products.csv` (product-specific lead time, current stock, and safety stock).



`test\_reorder.py` validates the reorder point calculation against known synthetic inputs.



\## Roadmap



\- \[x] Real transaction data cleaning and aggregation

\- \[x] Reorder point calculation

\- \[x] Readable report output

\- \[x] Unit tests

\- \[ ] Expand to more products

\- \[ ] Demand forecasting (moving average / simple regression)

\- \[ ] ABC analysis (classify products by sales volume)

\- \[ ] Telegram alerts for products needing reorder



\---



Built as part of a self-directed Python learning project, applying real-world data analysis to inventory management.

