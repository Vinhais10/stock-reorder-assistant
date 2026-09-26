# Stock Reorder Assistant

An interactive inventory management tool that calculates reorder points using real retail transaction data, flagging products that need restocking based on historical demand, supplier lead time, and safety stock.

Includes a **Streamlit dashboard** for visual, at-a-glance decision-making and a **conversational AI agent** that answers inventory questions in natural language.

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-dashboard-red.svg)
![Groq](https://img.shields.io/badge/agent-Groq%20%2B%20Llama%203.3-orange.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## What This Does

Retailers need to know when to reorder a product before it runs out, and how much to order, based on how fast it actually sells. This tool answers that question using a well-known supply chain formula, applied to real e-commerce transaction data:

    Reorder Point = (Average Daily Sales x Lead Time) + Safety Stock

If a product's current stock falls below its reorder point, it's flagged as needing restock.

## Features

- Loads and cleans 541,909 real transactions from the UCI "Online Retail" dataset
- Calculates average daily demand per product from historical sales
- Computes each product's reorder point using lead time and safety stock
- Interactive Streamlit dashboard: KPI cards, grouped bar chart, per-product status cards
- Conversational AI agent that answers questions using real data as tools
- Command-line report as an alternative to the dashboard
- Unit tested against synthetic data with known expected results

## Data Source

Sales data comes from the UCI Machine Learning Repository's "Online Retail" dataset (https://archive.ics.uci.edu/dataset/352/online+retail) - real, anonymized transactions from a UK-based online retailer (2010-2011).

Lead time and safety stock values are illustrative business parameters (the raw dataset has no supplier data), applied consistently to demonstrate the reorder logic.

## Tech Stack

- Python 3.14 - Core language
- pandas - Data loading, cleaning, aggregation
- openpyxl - Reading the source Excel file
- Streamlit - Interactive web dashboard
- Plotly - Charts
- Groq API - LLM for the conversational agent
- python-dotenv - Environment variable management

## Setup

1. Clone this repository:

    git clone https://github.com/Vinhais10/stock-reorder-assistant.git
    cd stock-reorder-assistant

2. Install dependencies:

    py -m pip install -r requirements.txt

3. Download the dataset from UCI and place Online Retail.xlsx in the project root.

4. Create a .env file with your Groq API key:

    GROQ_API_KEY=gsk_your_key_here

    Get a free key at https://console.groq.com/keys

5. Run the dashboard:

    py -m streamlit run app.py

    Or run the command-line report:

    py reorder.py

## Project Structure

    stock-reorder-assistant/
    ├── app.py                 # Streamlit dashboard + agent UI
    ├── reorder.py             # Core logic: data loading, cleaning, calculations
    ├── agent.py               # Conversational AI agent (Groq + Llama 3.3)
    ├── agent_tools.py         # Tools the agent can call (wraps reorder.py)
    ├── test_reorder.py        # Unit tests for reorder logic
    ├── test_agent_tools.py    # Sanity tests for agent tools
    ├── products.csv           # Product master data (lead time, stock, safety stock)
    ├── sales_history.csv      # Sample synthetic sales data (used for early testing)
    ├── requirements.txt
    ├── .env.example           # Template for API key
    ├── .gitignore
    └── README.md

## How It Works

1. reorder.py loads the raw Excel file, filters it to a set of target products, and cleans it - removing missing values and returns (negative quantities).
2. It calculates each product's average daily sales over the full transaction history.
3. It applies the reorder point formula, using per-product lead time and safety stock from products.csv.
4. app.py reuses this same logic to power a live Streamlit dashboard - no duplicated code between the CLI and the web app.
5. test_reorder.py validates the reorder point calculation against known synthetic inputs, independent of the real dataset.

## Conversational Agent

The project includes an AI agent that answers inventory questions in natural language, using real data from reorder.py as tools.

### How to use

Run the same Streamlit app:

    py -m streamlit run app.py

Then click the **Ask the Agent** tab. Ask things like:

- "Which products need reordering?"
- "Tell me about product 85123A"
- "Why is 85123A flagged?"
- "How has 85123A been selling in the last 30 days?"
- "What if the lead time for 85123A became 20 days?"

The agent responds in the language of the question (English or Portuguese).

### How it works

The agent uses **Groq** (Llama 3.3 70B) with **tool calling**. It never invents numbers - it calls Python functions from agent_tools.py, which reuse the existing logic in reorder.py.

Available tools:

- list_products_needing_reorder() - every flagged product
- get_product_info(product_id) - full details for one product
- get_reorder_point(product_id) - calculation breakdown
- get_sales_trend(product_id, days) - recent sales trend
- simulate_scenario(product_id, new_lead_time) - recalculate with a different lead time

## Dashboard

The app also includes a polished dashboard with:

- 4 KPI cards (products tracked, needs reorder, units in stock, days to stockout)
- Grouped bar chart comparing current stock vs reorder point
- Per-product cards with progress bars and status badges
- Toggle to filter only products that need reordering

## Roadmap

- [x] Real transaction data cleaning and aggregation
- [x] Reorder point calculation
- [x] Readable CLI report
- [x] Unit tests
- [x] Interactive Streamlit dashboard
- [x] Conversational AI agent with tool calling
- [x] Polished dark dashboard UI
- [ ] Expand to more products
- [ ] Demand forecasting (moving average / simple regression)
- [ ] ABC analysis (classify products by sales volume)
- [ ] Telegram alerts for products needing reorder
- [ ] Deploy to Streamlit Cloud
- [ ] Modular project structure (data/, tests/ folders)

## Note

This project uses a subset (4 products) of the full 541,909-row dataset to keep the demo focused and fast. The underlying logic scales to any number of products.

---

Built as part of a self-directed Python learning project, applying real-world data analysis to inventory management.
