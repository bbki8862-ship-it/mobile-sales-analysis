# 📱 Mobile Sales Analytics Platform (Big Data Analytics)

A complete Python-based Big Data Analytics system converted and enhanced from the original Power BI Mobile Sales Analytics project.

> **Original Repository Reference:** [Mobile-Sales-Analytics-PowerBI](https://github.com/moneshpondhekar/Mobile-Sales-Analytics-PowerBI)  
> *All original Power BI files, dashboards, images, and raw datasets are preserved intact.*

---

## 🌟 Project Overview
This project transitions business intelligence from a proprietary desktop tool (Power BI) into an open-source, scalable Python Big Data stack. It provides an end-to-end analytics workflow:
1. **Data Ingestion & Cleaning:** Standardizes dates, cleans categorical noise, validates numeric bounds, and engineers total sales revenue.
2. **Sales Analytics Engine:** Aggregates KPIs, brand performance, model sales, regional distribution, and time-series trends (MTD, YoY).
3. **Interactive UI Dashboard:** A modern, responsive multi-tab Streamlit web application powered by Plotly charts and dynamic multi-dimensional filters.
4. **Distributed Big Data Computing:** Demonstrates PySpark DataFrame transformations and Spark SQL for big data cluster scaling.
5. **The Five Vs of Big Data:** Rigorously analyzes Volume, Velocity, Variety, Veracity, and Value.

---

## 🗂️ Project Directory Structure

```text
bda-project/
├── app.py                              # Interactive Streamlit Web Application Dashboard
├── requirements.txt                    # Project dependencies (tested on Python 3.13)
├── README.md                           # Project documentation & execution guide
├── data/
│   ├── raw/
│   │   └── mobile_sales_data.csv       # Preserved original transactional dataset
│   └── processed/
│       └── mobile_sales_cleaned.csv    # Cleaned, validated, and feature-engineered dataset
├── src/
│   ├── __init__.py                     # Package initialization
│   ├── data_preprocessing.py           # Data cleaning, validation, and feature pipeline
│   ├── sales_analytics.py              # Statistical aggregations, KPIs, and Matplotlib plots
│   └── spark_analytics.py              # PySpark DataFrame operations and Spark SQL engine
├── notebooks/
│   ├── mobile_sales_analysis.ipynb     # Documented academic Jupyter Notebook
│   └── generate_notebook.py            # Reproducible script for generating the notebook
├── outputs/
│   └── figures/                        # High-resolution statistical PNG charts
│       ├── brand_revenue_distribution.png
│       ├── monthly_sales_trend.png
│       ├── city_sales_comparison.png
│       ├── payment_method_breakdown.png
│       └── customer_age_ratings_distribution.png
├── report/
│   └── PROJECT_REPORT.md               # Formal college project report
└── Mobile-Sales-Analytics-PowerBI/      # Preserved original Power BI repository
    ├── Mobile Sales Data.csv
    ├── README.md
    └── *.png
```

---

## 🚀 Key Metrics from the Verified Dataset

All figures are computed from the real 3,835 transaction records (2021–2024):

| Metric | Computed Value | Description |
| :--- | :--- | :--- |
| **Total Sales Revenue** | **₹769,204,987.97** (~₹769.20M) | Aggregate gross sales turnover |
| **Total Units Sold** | **19,150 units** | Physical smartphone devices sold |
| **Total Transactions** | **3,835 orders** | Verified distinct purchase records |
| **Average Selling Price (ASP)** | **₹40,114.04** | Mean price per smartphone unit |
| **Average Order Value (AOV)** | **₹200,574.96** | Average checkout transaction value |
| **Average Customer Rating** | **3.69 / 5.00** | Customer satisfaction score |
| **Top Brand by Revenue** | **Apple (₹161.62M)** | Followed closely by Samsung (₹160.04M) |
| **Top Payment Gateway** | **UPI & Credit Card** | Accounting for >60% of all transactions |

---

## 🚀 Step-by-Step Guide to Run This Project

Follow these exact steps in your terminal (PowerShell or Command Prompt) inside the project folder:

### Step 1: Install Required Dependencies
Install all required Python packages:
```powershell
pip install -r requirements.txt
```

### Step 2: Run Data Preprocessing Pipeline
Cleans the raw dataset, normalizes dates, validates values, calculates revenue, and saves the cleaned dataset to `data/processed/mobile_sales_cleaned.csv`:
```powershell
python src/data_preprocessing.py
```

### Step 3: Run Sales Analytics & Export Visualizations
Computes core KPIs and exports high-resolution statistical charts to `outputs/figures/`:
```powershell
python src/sales_analytics.py
```

### Step 4: Run Big Data PySpark Analytics (Distributed Spark SQL)
Executes distributed aggregations and Spark SQL queries:
```powershell
python src/spark_analytics.py
```

### Step 5: Launch the Interactive Streamlit Dashboard
Starts the web application dashboard in your browser:
```powershell
python -m streamlit run app.py
```
*Access the dashboard in your browser at: **http://localhost:8501***

### Step 6: Launch the Jupyter Notebook
Opens the comprehensive documented analysis notebook:
```powershell
python -m notebook notebooks/mobile_sales_analysis.ipynb
```

---

## 📊 Streamlit Dashboard Features
- **Executive KPI Cards:** Dynamic metrics formatted in Indian currency format (`₹ Cr`, `₹ Lakh`, `₹ M`).
- **Multi-Dimensional Sidebar Filters:** Dynamic filtering across Date Range, Brand, Mobile Model, City, and Payment Method with auto-synchronization.
- **7 Organized Navigation Tabs:**
  1. *Executive Summary:* Trajectory area chart, brand market share donut, and automated insights.
  2. *Brand & Model Performance:* Interactive bar charts, model rankings, and detailed performance matrix.
  3. *Time Trends & YoY:* Monthly trends, annual growth rates, and day-of-week heatmaps.
  4. *Geographic & Payments:* Top city rankings and payment gateway distribution.
  5. *Customer Analytics:* Age bracket revenue contribution and ratings boxplots.
  6. *Big Data & PySpark:* Detailed breakdown of the Five Vs and live PySpark execution trigger.
  7. *Data Explorer & Export:* Searchable data table with custom column selection and CSV download.

---

## 📄 Academic Project Report
A complete academic report covering objectives, the Five Vs, system architecture, mathematical formulations, and findings is available in:
📁 [PROJECT_REPORT.md](file:///report/PROJECT_REPORT.md)
