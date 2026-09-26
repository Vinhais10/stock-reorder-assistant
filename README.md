# 📦 Stock Reorder Assistant

An interactive inventory management tool that calculates reorder points using real retail transaction data, flagging products that need restocking based on historical demand, supplier lead time, and safety stock. Includes a Streamlit dashboard for visual, at-a-glance decision-making.

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-dashboard-red.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

---

# 📌 What This Does

Retailers need to know when to reorder a product before it runs out, and how much to order, based on how fast it actually sells. This tool answers that question using a well-known supply chain formula, applied to real e-commerce transaction data:

Reorder Point = (Average Daily Sales x Lead Time) + Safety Stock

If a product's current stock falls below its reorder point, it's flagged as needing restock.

---

# ✨ Features

- Loads and cleans 541,909 real transactions from the UCI "Online Retail" dataset
- Calculates average daily demand per product from historical sales
- Computes each product's reorder point using lead time and safety stock
- Interactive Streamlit dashboard: live metrics, per-product status cards, color-coded alerts
- Command-line report as an alternative to the dashboard
- Unit tested against synthetic data with known expected results

---

# 📊 Data Source

Sales data comes from the UCI Machine Learning Repository's "Online Retail" dataset (https://archive.ics.uci.edu/dataset/352/online+retail) - real, anonymized transactions from a UK-based online retailer (2010-2011).

Lead time and safety stock values are illustrative business parameters (the raw dataset has no supplier data), applied consistently to demonstrate the reorder logic.

---

# 🛠️ Tech Stack

- Python 3.14 - Core language
- pandas - Data loading, cleaning, aggregation
- openpyxl - Reading the source Excel file
- Streamlit - Interactive web dashboard

---

# 🚀 Setup

1. Clone this repository:

git clone https://github.com/Vinhais10/stock-reorder-assistant.git
cd stock-reorder-assistant

2. Install dependencies:

pip install -r requirements.txt

3. Download the dataset from UCI and place Online Retail.xlsx in the project root.

4. Run the dashboard:

streamlit run app.py

Or run the command-line report:

python reorder.py

---

# 📁 Project Structure

stock-reorder-assistant/
├── app.py                 # Streamlit dashboard
├── reorder.py              # Core logic: data loading, cleaning, calculations
├── test_reorder.py         # Unit tests
├── products.csv            # Product master data (lead time, stock, safety stock)
├── sales_history.csv       # Sample synthetic sales data (used for early testing)
├── requirements.txt
└── README.md

---

# 🧠 How It Works

1. reorder.py loads the raw Excel file, filters it to a set of target products, and cleans it - removing missing values and returns (negative quantities).
2. It calculates each product's average daily sales over the full transaction history.
3. It applies the reorder point formula, using per-product lead time and safety stock from products.csv.
4. app.py reuses this same logic to power a live Streamlit dashboard - no duplicated code between the CLI and the web app.
5. test_reorder.py validates the reorder point calculation against known synthetic inputs, independent of the real dataset.

---

# 🗺️ Roadmap

- [x] Real transaction data cleaning and aggregation
- [x] Reorder point calculation
- [x] Readable CLI report
- [x] Unit tests
- [x] Interactive Streamlit dashboard
- [ ] Expand to more products
- [ ] Demand forecasting (moving average / simple regression)
- [ ] ABC analysis (classify products by sales volume)
- [ ] Telegram alerts for products needing reorder
- [ ] Modular project structure (data/, tests/ folders)

---

# 📝 Note

This project uses a subset (4 products) of the full 541,909-row dataset to keep the demo focused and fast. The underlying logic scales to any number of products.

---

Built as part of a self-directed Python learning project, applying real-world data analysis to inventory management.
