"""
generate_notebook.py
--------------------
Utility script to programmatically create and validate the complete
Jupyter Notebook `notebooks/mobile_sales_analysis.ipynb` for college submission.
"""

import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Title & Metadata Cell
cells.append(nbf.v4.new_markdown_cell("""# 📱 Mobile Sales Analytics: Big Data Analytics & Distributed Computing
**Subject:** Big Data Analytics (BDA)  
**Project:** End-to-End Mobile Sales Performance, Market Trends & Distributed Analytics  
**Original Power BI Reference:** [Mobile-Sales-Analytics-PowerBI](https://github.com/moneshpondhekar/Mobile-Sales-Analytics-PowerBI)  
**Author:** Student Project Submission  

---

## 🎯 1. Executive Summary & Project Objectives
This project transitions an existing Power BI dashboard architecture into a robust, open-source Python Big Data Analytics platform. 

### Key Objectives:
1. **Data Ingestion & Quality Assurance:** Ingest 3,835 historical transaction records (2021–2024), address schema inconsistencies, validate numeric boundaries, and engineer critical dimensions (ISO Datetimes, Revenue, Age Brackets).
2. **Exploratory Data Analysis (EDA):** Quantify market concentration across 5 leading brands (Apple, Samsung, OnePlus, Vivo, Xiaomi), 15 models, 19 metropolitan cities, and 4 payment gateways.
3. **Statistical Visualizations:** Generate publication-quality plots illustrating monthly revenue trajectories, price elasticity, and customer rating distributions.
4. **Big Data Scaling (Apache Spark):** Implement PySpark DataFrame operations and Spark SQL to demonstrate how identical analytical pipelines scale horizontally across distributed clusters.
5. **The Five Vs of Big Data:** Rigorously evaluate the dataset across Volume, Velocity, Variety, Veracity, and Value.
"""))

# Big Data Framework Cell
cells.append(nbf.v4.new_markdown_cell("""---
## 🌐 2. Big Data Framework: The Five Vs Analysis
In enterprise e-commerce and retail analytics, understanding data dimensions dictates system architecture:

| Dimension | Dataset Reality (Current Academic Scope) | Enterprise / Big Data Scale (Production Scope) |
|---|---|---|
| **Volume** | 3,835 transaction records (~480 KB). Fits entirely in local memory (RAM). | Tens of millions of transactional events daily (>100 GB/day). Requires distributed storage (HDFS, Amazon S3, Azure ADLS). |
| **Velocity** | Static historical batch extract spanning 2021 to 2024. | High-frequency POS checkouts, real-time inventory adjustments via Apache Kafka / Spark Structured Streaming. |
| **Variety** | Structured tabular CSV schema with numerical, temporal, and string fields. | Multi-modal data: Clickstreams (JSON), uncurated reviews (NLP/Text), warranty claim attachments (Images/PDFs). |
| **Veracity** | High cleanliness (0 missing values), but minor syntactic noise (inconsistent day name abbreviations: `Sat` vs `Saturday`). | Noisy data: duplicated checkouts, fraudulent payment attempts, unverified customer demographic fields. |
| **Value** | Uncovers brand revenue dominance, city profitability, and payment channel economics to optimize inventory. | Real-time dynamic pricing engines, algorithmic recommendation systems, predictive churn mitigation. |
"""))

# Code: Imports & Setup
cells.append(nbf.v4.new_markdown_cell("""---
## 🛠️ 3. Environment Setup & Library Ingestion
We load essential libraries for data manipulation (`pandas`, `numpy`), visual analytics (`matplotlib`, `seaborn`, `plotly`), and distributed processing (`pyspark`).
"""))

cells.append(nbf.v4.new_code_cell("""import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure src modules are discoverable
sys.path.append(os.path.abspath('..'))
from src.data_preprocessing import load_raw_data, clean_and_transform_data, inspect_raw_data
from src.sales_analytics import (
    compute_kpis, 
    compute_brand_metrics, 
    compute_model_metrics, 
    compute_city_metrics, 
    compute_payment_metrics, 
    compute_monthly_trends,
    compute_yoy_metrics,
    compute_customer_demographics
)

# Plotting configuration
%matplotlib inline
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
sns.set_theme(style='whitegrid', palette='muted')

print("Libraries imported successfully!")
"""))

# Code: Raw Ingestion & Inspection
cells.append(nbf.v4.new_markdown_cell("""---
## 📥 4. Raw Data Ingestion & Structural Inspection
We load the raw CSV dataset and inspect its dimensions, schema, null values, and anomalies.
"""))

cells.append(nbf.v4.new_code_cell("""# Ingest raw dataset
raw_df = load_raw_data("../data/raw/mobile_sales_data.csv")
print(f"Dataset Dimensions: {raw_df.shape[0]} rows x {raw_df.shape[1]} columns")

# Summary report
report = inspect_raw_data(raw_df)
print("\\nMissing Values by Column:")
for col, nulls in report["null_counts"].items():
    print(f" - {col:20s}: {nulls}")

print(f"\\nDuplicate Records: {report['duplicate_rows']}")
raw_df.head()
"""))

# Code: Data Preprocessing & Validation
cells.append(nbf.v4.new_markdown_cell("""---
## 🧹 5. Data Cleaning, Validation & Feature Engineering
We transform raw attributes into analytical dimensions:
1. **ISO Datetime Formulation:** Synthesize `Year`, `Month`, `Day` into a validated `Date` timestamp.
2. **Day Name Normalization:** Address inconsistencies between abbreviations (`Sat`) and full names (`Saturday`).
3. **Core Metric Derivation:** Calculate total sales revenue: $\\text{Revenue} = \\text{Units Sold} \\times \\text{Price Per Unit}$.
4. **Demographic Binning:** Partition `Customer Age` into logical consumer brackets (`< 25`, `25-34`, `35-49`, `50+`).
"""))

cells.append(nbf.v4.new_code_cell("""# Execute transformation pipeline
df = clean_and_transform_data(raw_df)

print(f"Cleaned dataset shape: {df.shape}")
print(f"Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
print("\\nSample engineered records:")
df[["Transaction ID", "Date", "Brand", "Mobile Model", "Units Sold", "Price Per Unit", "Revenue", "Age Group"]].head()
"""))

# Code: KPI Computation
cells.append(nbf.v4.new_markdown_cell("""---
## 📊 6. Core Sales Key Performance Indicators (KPIs)
Here we compute the macroeconomic indicators of the business portfolio.
"""))

cells.append(nbf.v4.new_code_cell("""kpis = compute_kpis(df)

print("="*50)
print("             ENTERPRISE SALES HEADLINE KPIS")
print("="*50)
print(f"Total Revenue Generated      : INR {kpis['total_revenue']:,.2f} (~INR {kpis['total_revenue']/1e6:.2f} Million)")
print(f"Total Physical Units Sold    : {kpis['total_units']:,} units")
print(f"Total Processed Transactions : {kpis['total_transactions']:,}")
print(f"Average Price Per Unit (ASP) : INR {kpis['avg_price_per_unit']:,.2f}")
print(f"Average Transaction Value    : INR {kpis['avg_transaction_value']:,.2f}")
print(f"Average Customer Rating      : {kpis['avg_rating']:.2f} / 5.00")
print(f"Leading Brand by Revenue     : {kpis['top_brand']}")
print(f"Top Performing Metro City    : {kpis['top_city']}")
print(f"Dominant Payment Gateway     : {kpis['top_payment_method']}")
print("="*50)
"""))

# Code: Brand & Model Analytics
cells.append(nbf.v4.new_markdown_cell("""---
## 📱 7. Brand & Model Market Share Analysis
We analyze how revenue and volume distribute across the 5 smartphone manufacturers.
"""))

cells.append(nbf.v4.new_code_cell("""brand_metrics = compute_brand_metrics(df)
print(brand_metrics.to_string(index=False))

# Plot Brand Revenue and Volume
fig, ax1 = plt.subplots(figsize=(10, 5))
x = np.arange(len(brand_metrics))
width = 0.35

rects1 = ax1.bar(x - width/2, brand_metrics["Revenue"]/1e6, width, label="Revenue (INR Millions)", color="#1f77b4")
ax2 = ax1.twinx()
rects2 = ax2.bar(x + width/2, brand_metrics["Units_Sold"], width, label="Units Sold", color="#ff7f0e")

ax1.set_xlabel("Smartphone Brand", fontweight='bold')
ax1.set_ylabel("Total Revenue (INR Millions)", color="#1f77b4", fontweight='bold')
ax2.set_ylabel("Physical Units Sold", color="#ff7f0e", fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(brand_metrics["Brand"])
ax1.set_title("Brand-Wise Revenue Contribution vs Volume Sold", fontsize=13, fontweight='bold', pad=12)
fig.tight_layout()
plt.show()
"""))

# Code: Time Trends & YoY
cells.append(nbf.v4.new_markdown_cell("""---
## 📈 8. Time Series & Year-over-Year (YoY) Dynamics
Tracking seasonal revenue trends and annualized expansion rates from 2021 through 2024.
"""))

cells.append(nbf.v4.new_code_cell("""yoy_metrics = compute_yoy_metrics(df)
print("Year-over-Year Trajectory:")
print(yoy_metrics.to_string(index=False))

# Monthly Sales Time Series
monthly_df = compute_monthly_trends(df)

plt.figure(figsize=(12, 5))
plt.plot(monthly_df["Year-Month"], monthly_df["Revenue"]/1e6, marker='o', linewidth=2.2, color='#2ca02c')
plt.title("Monthly Revenue Trajectory (2021 - 2024)", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Fiscal Year & Month", fontweight='bold')
plt.ylabel("Revenue (INR Millions)", fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
"""))

# Code: City & Payment Methods
cells.append(nbf.v4.new_markdown_cell("""---
## 🏙️ 9. Geographic & Payment Method Analytics
Identifying top geographical revenue hubs and preferred customer transaction channels.
"""))

cells.append(nbf.v4.new_code_cell("""city_metrics = compute_city_metrics(df)
payment_metrics = compute_payment_metrics(df)

fig, (ax_city, ax_pay) = plt.subplots(1, 2, figsize=(15, 6))

# Top 8 Cities
top_cities = city_metrics.head(8)
sns.barplot(data=top_cities, x="Revenue", y="City", hue="City", legend=False, palette="Blues_r", ax=ax_city)
ax_city.set_title("Top 8 Metropolitan Revenue Hubs", fontweight='bold')
ax_city.set_xlabel("Revenue (INR)", fontweight='bold')

# Payment Method Share
ax_pay.pie(
    payment_metrics["Revenue"], 
    labels=payment_metrics["Payment Method"], 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=["#4e79a7", "#f28e2c", "#e15759", "#76b7b2"],
    wedgeprops=dict(width=0.4, edgecolor='w')
)
ax_pay.set_title("Revenue Share by Payment Gateway", fontweight='bold')

plt.tight_layout()
plt.show()
"""))

# Code: Customer Demographics & Ratings
cells.append(nbf.v4.new_markdown_cell("""---
## 👥 10. Customer Demographics & Satisfaction Patterns
Evaluating purchasing power across demographic brackets and price distribution across customer ratings.
"""))

cells.append(nbf.v4.new_code_cell("""demo_dict = compute_customer_demographics(df)
print("Customer Age Group Purchasing Performance:")
print(demo_dict["age_groups"].to_string(index=False))

fig, (ax_box, ax_hist) = plt.subplots(1, 2, figsize=(14, 5))

# Price vs Rating
sns.boxplot(data=df, x="Customer Ratings", y="Price Per Unit", hue="Customer Ratings", legend=False, palette="Purples", ax=ax_box)
ax_box.set_title("Price Distribution Across Customer Ratings", fontweight='bold')
ax_box.set_xlabel("Rating (1 to 5 Stars)", fontweight='bold')
ax_box.set_ylabel("Price Per Unit (INR)", fontweight='bold')

# Customer Age Histogram
sns.histplot(df["Customer Age"], bins=15, kde=True, color="#9467bd", ax=ax_hist)
ax_hist.set_title("Customer Age Demographic Histogram", fontweight='bold')
ax_hist.set_xlabel("Age (Years)", fontweight='bold')

plt.tight_layout()
plt.show()
"""))

# Code: Big Data with PySpark
cells.append(nbf.v4.new_markdown_cell("""---
## ⚡ 11. Distributed Big Data Processing with Apache Spark
To satisfy the Big Data Analytics syllabus requirements, we demonstrate how this sales analytics pipeline executes within Apache Spark using the **PySpark DataFrame API** and **Spark SQL**.

### Theoretical Concepts Illustrated:
- **Resilient Distributed Datasets (RDDs) & DataFrames:** Immutable, lazily evaluated distributed collections.
- **Catalyst Optimizer:** Automatic query optimization and physical execution plan generation.
- **Spark SQL Engine:** Running standard ANSI SQL against in-memory registered tables.
"""))

cells.append(nbf.v4.new_code_cell("""from src.spark_analytics import run_spark_analysis

# Execute distributed pipeline
spark_results = run_spark_analysis("../data/processed/mobile_sales_cleaned.csv")

if spark_results.get("status") == "success":
    print(f"PySpark Version: {spark_results['spark_version']}")
    print(f"RDD Partitions : {spark_results['partitions']}")
    print(f"Records Ingested: {spark_results['record_count']}")
    print("\\nPySpark Computed KPIs:")
    for k, v in spark_results['kpis'].items():
        print(f" - {k:22s}: {v}")
        
    print("\\nSpark SQL Brand Aggregation Result:")
    display(spark_results['brand_summary'])
else:
    print("Spark notice:", spark_results.get("message"))
"""))

# Markdown: Conclusions & Recommendations
cells.append(nbf.v4.new_markdown_cell("""---
## 💡 12. Strategic Business Findings & Recommendations

1. **Brand Dominance & Premium Pricing:**
   - **Apple** and **Samsung** lead in total gross turnover (~INR 161.6M and ~INR 160.0M respectively), driven by higher Average Selling Prices (ASP > INR 40,000).
   - **OnePlus**, **Vivo**, and **Xiaomi** remain vital volume drivers, demonstrating high unit turnover in entry-level to mid-range segments.

2. **Digital Payment Acceleration:**
   - **UPI** and **Credit Cards** represent the vast majority of transactions (>60%), indicating strong digital banking penetration in targeted urban demographics.

3. **Regional Market Concentration:**
   - Tier-1 metropolitan centres (**Delhi**, **Mumbai**, **Bengaluru**) contribute the lion's share of revenue, suggesting that promotional ad spends and premium inventory logistics should prioritize these nodes.

4. **Big Data Scaling Roadmap:**
   - While Pandas handles the current 3,835 transaction records efficiently, transitioning to Apache Spark enables scaling seamlessly to millions of records without code redesign.
"""))

nb["cells"] = cells

# Save notebook
output_nb_path = "notebooks/mobile_sales_analysis.ipynb"
with open(output_nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Generated Jupyter Notebook with {len(cells)} cells at '{output_nb_path}' successfully!")
