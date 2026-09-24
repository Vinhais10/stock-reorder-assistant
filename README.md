📦 Stock Reorder Assistant
A proof-of-concept inventory analysis tool that uses historical retail transaction data to support stock replenishment decisions.

https://img.shields.io/badge/Python-3.10%2B-blue
https://img.shields.io/badge/Streamlit-App-red
https://img.shields.io/badge/License-MIT-green
https://img.shields.io/badge/Status-Proof%20of%20Concept-orange

📌 Business Problem
Businesses need to determine:

When should a product be reordered?

How much stock should be maintained?

Which products are at risk of stockout?

Poor inventory decisions can lead to:

Lost sales

Excess inventory

Higher storage costs

Operational inefficiencies

This project demonstrates a simple, data-driven approach to support inventory replenishment decisions.

📊 Dataset
This project uses the Online Retail Dataset from the UCI Machine Learning Repository.

📈 Dataset Overview
541,909 retail transactions

Real-world data from a UK-based online retailer

Time period: 01/12/2010 – 09/12/2011

The retailer specialises in all-occasion gift-ware, selling mainly to wholesalers

The company's identity is anonymised for commercial privacy reasons — the numbers are real, the brand name is not disclosed

🧾 Columns
Column	Description
InvoiceNo	Invoice number (cancellations start with "C")
StockCode	Product code
Description	Product name
Quantity	Units sold per transaction
InvoiceDate	Date and time of sale
UnitPrice	Price per unit
CustomerID	Customer identifier
Country	Customer country

⚠️ Data Quality Notes
Real data is messy — and handling that is part of the exercise. The raw dataset contains:

Missing CustomerID values

Cancelled orders (invoices starting with "C")

Negative quantities (returns)

Zero or negative unit prices

These are handled during the preprocessing stage.

🧠 Approach
Data Cleaning — remove cancellations, returns, and nulls

Feature Engineering — aggregate sales per product

Demand Analysis — calculate average daily/weekly demand

Reorder Logic — apply a simple reorder point formula:

text
Reorder Point = (Average Daily Demand × Lead Time) + Safety Stock
Risk Flagging — identify products below the reorder point

🧪 Development Discipline: Synthetic First, Real Later
The project intentionally started with fabricated data before moving to the real dataset — the same technique used in the RSI project. Testing logic with numbers you already know in advance makes it far easier to catch calculation errors than debugging against thousands of unpredictable real rows.

Once the logic was confirmed working (numbers matched), the project advanced to real data. This is not "less professional" — it is development discipline.

🚀 Getting Started
Prerequisites
Python 3.10+

pip

Installation
bash
git clone https://github.com/<your-username>/stock-reorder-assistant.git
cd stock-reorder-assistant
pip install -r requirements.txt
Downloading the Dataset
Go to the UCI Online Retail page

Click Download — this brings a .zip file

Extract it — inside is Online Retail.xlsx (Excel, not CSV)

Move Online Retail.xlsx into the stock-reorder-assistant folder

Note: pandas alone cannot read .xlsx files. Install the extra "translator":

bash
py -m pip install openpyxl
Running the App
bash
streamlit run app.py
The server will start and print:

text
Uvicorn server started
You can now view your Streamlit app in your browser: http://localhost:8501
This is not an error — it means Streamlit is up and waiting. If the browser does not open automatically, open it manually and go to:

text
http://localhost:8501
⚠️ Important: do not close the PowerShell window while using the app — that window is the server keeping it alive.

You should see the 📦 Stock Reorder Assistant dashboard, the metric of products needing reorder, and the product cards with red "REORDER NEEDED" badges.

📁 Project Structure
text
stock-reorder-assistant/
├── app.py                  # Streamlit dashboard
├── reorder.py              # Core reorder logic
├── explore.py              # Dataset exploration script
├── test_reorder.py         # Logic tests (synthetic data)
├── products.csv            # Lead time + safety stock per product
├── sales_history.csv       # Sales history (test → replaced by real data)
├── Online Retail.xlsx      # Real UCI dataset (not committed)
├── requirements.txt
├── .gitignore
└── README.md

📄 File Roles
File	Purpose
products.csv	Fabricated — contains lead_time_days and safety_stock, which the UCI dataset does not provide
sales_history.csv	Initially synthetic for logic testing; to be replaced by a filtered sample of the real UCI data (3–4 chosen products)
reorder.py	The reorder point calculation and risk flagging
app.py	Streamlit front-end showing metrics and product cards

📤 Example Output
StockCode	Description	Avg Daily Demand	Reorder Point	Current Stock	Action
85123A	WHITE HANGING HEART T-LIGHT HOLDER	12.4	87	52	🔴 REORDER NEEDED
71053	WHITE METAL LANTERN	3.1	22	40	🟢 OK
84406B	CREAM CUPID HEARTS COAT HANGER	8.7	61	15	🔴 REORDER NEEDED
84029G	KNITTED UNION FLAG HOT WATER BOTTLE	1.9	14	30	🟢 OK

🛠️ Tech Stack
pandas — data manipulation

numpy — numerical operations

openpyxl — reading .xlsx files

streamlit — interactive dashboard

🔮 Future Improvements
□ Replace sales_history.csv with a filtered sample of the real UCI dataset
□ Integrate supplier lead times per product
□ Add seasonality detection (e.g. Prophet, ARIMA)
□ Support multiple warehouses
□ Add unit tests with pytest
□ Reorganise into data/ and tests/ folders

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

📄 License
This project is licensed under the MIT License.

🙏 Acknowledgements
UCI Machine Learning Repository for hosting the dataset

Dr. Daqing Chen — creator of the Online Retail dataset

📌 A Note on Dataset Authenticity
Several Kaggle datasets use famous brand names (e.g. "ZARA Sales") but are often synthetic or scraped catalogue data, not verified real sales. Since the Inditex group (Zara, Massimo Dutti, etc.) is a private company, its real sales data is confidential and not publicly available.

For this reason, this project uses the UCI Online Retail dataset — academically documented, genuinely real, and ethically shared. It is not specifically fashion retail, but the inventory logic is identical across sectors: whether the product is a decorative mug or a Massimo Dutti sweater, average demand and reorder points are calculated the same way.

📋 Quick Commands Reference
bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py

# Run logic tests
python test_reorder.py

# Explore the dataset
python explore.py

# Git workflow
git add .
git commit -m "Update README"
git push
