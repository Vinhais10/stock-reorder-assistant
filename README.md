\# 📦 Stock Reorder Assistant



A proof-of-concept inventory analysis tool that uses historical retail transaction data to support stock replenishment decisions.



The project explores how historical sales data can be transformed into practical inventory metrics and used to identify products that may require replenishment.



\---



\## 📌 Business Problem



Inventory management requires businesses to balance product availability with the cost of holding excess stock.



Key questions include:



\- When should a product be reordered?

\- Which products may be at risk of stockout?

\- How can historical demand support replenishment decisions?

\- How can inventory decisions be made more consistently using data?



This project demonstrates a simple data-driven approach to inventory replenishment using historical retail transaction data.



\---



\## 📊 Dataset



This project uses the \*\*Online Retail Dataset\*\* from the \*\*UCI Machine Learning Repository\*\*.



The dataset contains real-world retail transaction data from an online retail business.



\### Dataset Overview



\- \*\*541,909\*\* transactions

\- \*\*8\*\* original attributes

\- Product codes and descriptions

\- Transaction dates

\- Quantities sold

\- Unit prices

\- Customer information

\- Country information



\### Source



\*\*UCI Machine Learning Repository — Online Retail Dataset\*\*



https://archive.ics.uci.edu/dataset/352/online+retail



\---



\## 🚀 Features



\### 🔎 Data Exploration



\- Load and analyse historical retail transactions

\- Explore product-level sales data

\- Identify top-selling products

\- Aggregate sales quantities by product

\- Prepare historical sales data for inventory analysis



\### 📦 Inventory Analytics



\- Calculate average daily demand

\- Estimate reorder points

\- Support safety stock calculations

\- Compare current stock against reorder thresholds

\- Identify products requiring replenishment



\### 📈 Interactive Dashboard



The project includes a \*\*Streamlit dashboard\*\* for interactive inventory analysis.



The dashboard provides:



\- Inventory overview

\- Product-level information

\- Current stock status

\- Reorder status

\- Sales analysis

\- Reorder recommendations



\### 🧪 Testing



The core reorder logic is supported by automated tests using \*\*pytest\*\*.



The goal is to ensure that the business rules used by the application behave as expected.



\---



\## 🧮 Reorder Model



The current proof of concept uses a simple \*\*Reorder Point\*\* model.



\### Reorder Point



```text

Reorder Point = Average Daily Sales × Lead Time + Safety Stock



A product is flagged for replenishment when:



Current Stock ≤ Reorder Point



This provides a simple and transparent rule for identifying products that may require a new order.



The model is intentionally kept simple at this stage, as the main objective of the project is to demonstrate the connection between historical sales data, inventory analysis and business decision support.



🖥️ Application



The project includes an interactive Streamlit dashboard designed to make the analysis easier to explore.



The application allows users to move from raw sales data to product-level inventory insights.



Dashboard Areas

Dashboard — Overview of the inventory

Inventory — Product and stock information

Reorder Analysis — Reorder point and replenishment logic

Sales Analysis — Historical sales behaviour

Reorder Recommendations — Products identified for replenishment



📸 Application screenshots will be added as the dashboard develops.



🗂️ Project Structure

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

🛠️ Technologies

Technology	Purpose

Python	Core programming language

pandas	Data analysis and data transformation

Streamlit	Interactive dashboard

openpyxl	Excel data processing

pytest	Automated testing

Git	Version control

GitHub	Source control and project documentation

⚙️ Installation

1\. Clone the repository

git clone https://github.com/Vinhais10/stock-reorder-assistant.git

2\. Navigate to the project directory

cd stock-reorder-assistant

3\. Install the required dependencies

pip install -r requirements.txt

▶️ Running the Application



Start the Streamlit dashboard with:



streamlit run app.py



The application will normally be available at:



http://localhost:8501

🧪 Running Tests



Run the automated test suite with:



pytest

🔄 Project Workflow



The overall workflow can be summarised as:



Historical Retail Data

&#x20;       ↓

Data Exploration

&#x20;       ↓

Sales Analysis

&#x20;       ↓

Demand Estimation

&#x20;       ↓

Inventory Metrics

&#x20;       ↓

Reorder Point

&#x20;       ↓

Reorder Recommendation

&#x20;       ↓

Streamlit Dashboard



This structure separates data analysis, business logic and presentation, making the project easier to extend as new features are introduced.



📌 Current Status



Proof of Concept (PoC)



The current version focuses on demonstrating how historical retail transaction data can be used to support inventory replenishment decisions.



The application is still under development.



The current implementation prioritises:



Clear business logic

Real-world transaction data

Simple and explainable inventory calculations

Interactive data exploration

Automated testing

🔮 Future Improvements



Potential future improvements include:



&#x20;Dynamic safety stock calculation

&#x20;Demand forecasting

&#x20;Supplier lead-time modelling

&#x20;Product-level demand trends

&#x20;Seasonal demand analysis

&#x20;Improved dashboard visualisations

&#x20;Exportable inventory reports

&#x20;Database integration

&#x20;More extensive automated testing

&#x20;Improved reorder quantity recommendations

⚠️ Disclaimer



This project is an independent proof of concept created for educational and portfolio purposes.



The inventory recommendations generated by the application are based on simplified assumptions and should not be considered production-ready inventory management decisions.



The dataset is provided by the UCI Machine Learning Repository and is used for analytical and educational purposes.



👨‍💻 Author



Diogo Vinhais



Management Informatics @ ISCAC



Python • Data Analytics • Process Automation

