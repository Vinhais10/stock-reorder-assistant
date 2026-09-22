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

2\. Install dependencies:

&#x20;  ```bash

&#x20;  pip install pandas openpyxl

