\# 📦 Stock Reorder Assistant



A proof-of-concept inventory analysis tool that uses historical retail transaction data to support stock replenishment decisions.



This project explores how historical sales data can be transformed into simple inventory metrics such as average demand, safety stock and reorder points.



The application includes an interactive Streamlit dashboard for exploring products, sales behaviour and reorder recommendations.



\---



\## Business Problem



Businesses need to determine:



\* When should a product be reordered?

\* How much stock should be maintained?

\* Which products are at risk of stockout?



Poor inventory decisions can lead to:



\* Lost sales

\* Excess inventory

\* Higher storage costs

\* Operational inefficiencies



This project demonstrates a simple data-driven approach to support inventory replenishment decisions.



\---



\## Dataset



This project uses the \*\*Online Retail Dataset\*\* from the UCI Machine Learning Repository:



\* 541,909 retail transactions

\* Real sales data

\* Product information

\* Transaction dates

\* Quantities sold

\* Customer and country information



Dataset source:



https://archive.ics.uci.edu/dataset/352/online+retail



\---



\## Features



\### Data Exploration



\* Load and analyse retail transaction data

\* Identify top-selling products

\* Explore sales behaviour



\### Inventory Analytics



\* Average daily sales calculation

\* Reorder point calculation

\* Safety stock support

\* Reorder decision logic



\### Interactive Dashboard



\* Inventory overview

\* Product status

\* Reorder recommendations

\* Sales analysis



\### Quality



\* Automated tests

\* Modular project structure

\* Reproducible workflow



\---



\## Reorder Model



The current proof of concept uses a simple reorder point approach:



Reorder Point =



Average Daily Sales × Lead Time + Safety Stock



A reorder recommendation is generated when:



Current Stock ≤ Reorder Point



\---



\## Project Structure



```text

stock-reorder-assistant/

│

├── app.py

├── reorder.py

├── explore.py

│

├── data/

│   ├── products.csv

│   └── sales\_history.csv

│

├── tests/

│   └── test\_reorder.py

│

├── README.md

├── requirements.txt

└── .gitignore

```



\---



\## Technologies



\* Python

\* pandas

\* Streamlit

\* openpyxl

\* pytest

\* Git

\* GitHub



\---



\## Installation



Clone the repository:



```bash

git clone https://github.com/Vinhais10/stock-reorder-assistant.git

cd stock-reorder-assistant

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\---



\## Running the Project



Run the Streamlit dashboard:



```bash

streamlit run app.py

```



Open:



```text

http://localhost:8501

```



\---



\## Running Tests



```bash

pytest

```



\---



\## Current Status



Proof of Concept (PoC)



The current implementation focuses on demonstrating inventory replenishment concepts using historical retail data and a simple reorder point model.



Future improvements may include:



\* Dynamic safety stock

\* Demand forecasting

\* Supplier lead-time modelling

\* Database integration

\* Exportable reports

\* Enhanced visualisations



\---



\## Author



Diogo Vinhais



Management Informatics @ ISCAC



Python • Data Analytics • Process Automation



