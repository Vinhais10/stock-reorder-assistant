# \# 📦 **Stock Reorder Assistant**



A proof-of-concept inventory analysis tool that uses historical retail transaction data to support stock replenishment decisions.



\---



##### \## 📌 **Business Problem**



Businesses need to determine:



\- When should a product be reordered?

\- How much stock should be maintained?

\- Which products are at risk of stockout?



Poor inventory decisions can lead to:



\- Lost sales

\- Excess inventory

\- Higher storage costs

\- Operational inefficiencies



This project demonstrates a simple data-driven approach to support inventory replenishment decisions.



\---

##### 

##### **## 📊 Dataset**



This project uses the \*\*Online Retail Dataset\*\* from the UCI Machine Learning Repository.



\### Dataset Overview



\- \*\*541,909\*\* retail transactions

\- Real-world retail transaction data

\- Product information

\- Transaction dates

\- Quantities sold

\- Unit prices

\- Customer information

\- Country information



Dataset source:



https://archive.ics.uci.edu/dataset/352/online+retail



\---



##### **## 🚀 Features**



\### 🔎 Data Exploration



\- Analyse historical retail transactions

\- Identify top-selling products

\- Explore sales behaviour

\- Aggregate sales by product



##### **### 📦 Inventory Analytics**



\- Calculate average daily demand

\- Calculate reorder points

\- Support safety stock calculations

\- Identify products requiring replenishment

##### 

##### **### 📈 Interactive Dashboard**



The project includes a Streamlit dashboard for exploring:



\- Inventory status

\- Product information

\- Sales behaviour

\- Reorder recommendations



##### **### 🧪 Testing**



\- Automated tests for the reorder logic

\- Validation of core business rules



\---

##### 

##### **## 🧮 Reorder Model**



The current proof of concept uses a simple reorder point model.



\### Reorder Point



```text

Reorder Point = Average Daily Sales × Lead Time + Safety Stock





A product is flagged for replenishment when:



Current Stock ≤ Reorder Point



This approach provides a simple and transparent way of supporting inventory decisions based on historical demand.

##### 

##### 🖥️ Application



The project includes an interactive Streamlit dashboard.



The dashboard allows users to explore product-level inventory information and identify products that may require replenishment.



📸 Screenshots will be added as the application develops.

##### 

##### **🗂️ Project Structure**

**stock-reorder-assistant/**

**│**

**├── app.py**

**├── reorder.py**

**├── explore.py**

**│**

**├── data/**

**│   ├── products.csv**

**│   └── sales\_history.csv**

**│**

**├── tests/**

**│   └── test\_reorder.py**

**│**

**├── README.md**

**├── requirements.txt**

**└── .gitignore**

##### 

##### **🛠️ Technologies**

**Technology	Purpose**

**Python	Core programming language**

**pandas	Data analysis and transformation**

**Streamlit	Interactive dashboard**

**openpyxl	Excel data processing**

**pytest	Automated testing**

**Git	Version control**

**GitHub	Repository and project documentation**



##### **⚙️ Installation**



**Clone the repository:**



**git clone https://github.com/Vinhais10/stock-reorder-assistant.git**

**cd stock-reorder-assistant**



**Install the required dependencies:**



**pip install -r requirements.txt**

##### 

##### **▶️ Running the Application**



**Start the Streamlit application:**



**streamlit run app.py**



**Then open:**



**http://localhost:8501**



##### **🧪 Running Tests**



**Run the test suite with:**



**pytest**



##### **📌 Current Status**



**Proof of Concept (PoC)**



**The current version focuses on demonstrating how historical sales data can be used to support inventory replenishment decisions.**



**The project is still under development.**



##### **🔮 Future Improvements**



**Possible future improvements include:**



&#x20;**Dynamic safety stock calculation**

&#x20;**Demand forecasting**

&#x20;**Supplier lead-time modelling**

&#x20;**Product-level demand trends**

&#x20;**Improved dashboard visualisations**

&#x20;**Exportable inventory reports**

&#x20;**Database integration**

&#x20;**More extensive automated testing**

##### 

##### **👨‍💻 Author**



**Diogo Vinhais**



**Management Informatics @ ISCAC**



**Python • Data Analytics • Process Automation**

