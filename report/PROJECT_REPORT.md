# Academic Project Report: Mobile Sales Analytics Platform
**Subject:** Big Data Analytics (BDA)  
**Project Title:** End-to-End Mobile Sales Analytics and Interactive Decision Support System Using Python and Apache Spark  
**Reference Source:** Converted and enhanced from [Power BI Mobile Sales Analytics](https://github.com/moneshpondhekar/Mobile-Sales-Analytics-PowerBI)  
**Academic Year:** 2026  

---

## 1. Aim and Objectives

### 1.1 Aim
To re-engineer an existing enterprise Power BI sales reporting dashboard into a scalable, reproducible, open-source Big Data Analytics (BDA) system utilizing Python, Pandas, Matplotlib, Seaborn, Plotly, Streamlit, and Apache Spark (PySpark).

### 1.2 Objectives
1. **Data Ingestion & Integrity Auditing:** Ingest the raw mobile sales transactional dataset (3,835 records spanning 2021 to 2024), detect schema anomalies, and conduct quality assurance.
2. **Data Preprocessing & Feature Engineering:** Clean inconsistent categorical attributes (such as weekday abbreviations), construct standardized ISO timestamps, validate numerical constraints, and engineer business indicators (Total Revenue, Age Brackets, Quarterly Periods).
3. **Exploratory Data Analysis (EDA):** Quantify market performance across 5 smartphone manufacturers (Apple, Samsung, OnePlus, Vivo, Xiaomi), 15 models, 19 metropolitan cities, and 4 payment gateways.
4. **Interactive Decision-Support UI:** Develop a responsive, web-based analytical dashboard using Streamlit and Plotly with dynamic multi-dimensional slicing.
5. **Distributed Processing Demonstration:** Demonstrate how the transactional analytical pipeline scales to big data architectures using PySpark DataFrames and Spark SQL.
6. **Theoretical Big Data Evaluation:** Rigorously evaluate the project against the foundational Five Vs of Big Data (Volume, Velocity, Variety, Veracity, Value).

---

## 2. Big Data Framework: The Five Vs Analysis

To maintain academic and professional honesty, the dataset is evaluated against both its current academic scope and an enterprise production architecture:

| The 5 Vs | Current Academic Dataset Reality | Enterprise Big Data Production Scope |
| :--- | :--- | :--- |
| **Volume (Scale)** | **3,835 transactional records (~480 KB)**. Operates in-memory (RAM) on a single workstation via Pandas. | Tens of millions of POS checkout events generated daily (>100 GB/day). Demands distributed storage (HDFS, Ceph, Amazon S3, Azure Blob). |
| **Velocity (Speed)** | Static historical batch extract covering 2021-10-09 to 2024-10-08. No continuous real-time streaming ingested. | Sub-second event ingestion via Apache Kafka, Amazon Kinesis, and continuous aggregation using Spark Structured Streaming. |
| **Variety (Format)** | Structured tabular CSV format consisting of 14 standard numerical, temporal, and categorical attributes. | Multi-modal heterogeneous sources: Clickstream logs (JSON), uncurated customer reviews (NLP text), product manuals (PDF), social sentiment feeds. |
| **Veracity (Truth)** | **High integrity:** 0 null values, 0 duplicate rows. Minor syntactic noise: mixed weekday abbreviations (`Sat` vs `Saturday`) resolved via datetime parsing. | High noise: network latency duplicates, incomplete checkouts, fraudulent transactions, corrupted device telemetry. |
| **Value (Impact)** | Identifies market revenue leaders (Apple ₹161.6M, Samsung ₹160.0M), high-revenue hubs (Delhi, Mumbai), and UPI digital dominance (42%). | Real-time dynamic pricing, automated replenishment supply chains, predictive fraud detection, personalized recommendation engines. |

---

## 3. System Architecture and Technologies Used

The application is structured into decoupled, modular tiers:

```
+---------------------------------------------------------------------------------+
|                                 USER INTERFACE                                  |
|         Streamlit Multi-Tab Web Application (Responsive Dashboard & UI)         |
|             - KPI Metric Cards        - Interactive Plotly Visuals              |
|             - Multi-Select Slicers    - Dynamic Filtered Data Table Export      |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                               ANALYTICS ENGINE                                  |
|     src/sales_analytics.py                     src/spark_analytics.py           |
|     - Pandas & NumPy Calculations              - PySpark 4.2.0 DataFrame API    |
|     - Time-Series Trends (YoY, MTD)            - Catalyst Query Optimizer       |
|     - Static Figures (Matplotlib/Seaborn)      - Spark SQL In-Memory Engine     |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                           PREPROCESSING & VALIDATION                            |
|                            src/data_preprocessing.py                            |
|     - Ingestion & Type Casting                 - Revenue Computation            |
|     - Datetime ISO Normalization               - Demographic Bracket Binning    |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                                DATA REPOSITORY                                  |
|     Raw: data/raw/mobile_sales_data.csv                                         |
|     Cleaned: data/processed/mobile_sales_cleaned.csv                             |
+---------------------------------------------------------------------------------+
```

### Technology Stack Details:
- **Python 3.13:** Core execution environment.
- **Pandas 2.x & NumPy:** In-memory vector arithmetic, dataset manipulation, and grouping.
- **Matplotlib 3.x & Seaborn:** Statistical chart generation and publication-ready PNG outputs.
- **Streamlit 1.30+:** Interactive web application framework for dashboard delivery.
- **Plotly 7.x:** Dynamic client-side chart rendering (pie, area, bar, box, heatmap).
- **Jupyter Notebook (`nbformat`):** Educational step-by-step experimentation notebook.
- **Apache Spark (PySpark 4.2.0):** Distributed DataFrame operations and Spark SQL demonstrations.

---

## 4. Dataset Schema & Data Dictionary

| Column Name | Raw Type | Cleaned Type | Description |
| :--- | :--- | :--- | :--- |
| `Transaction ID` | `int64` | `int64` | Unique transaction sequence identifier (1 to 3835). |
| `Date` | *Derived* | `datetime64[ns]` | Standardized calendar timestamp (`YYYY-MM-DD`). |
| `Day` | `int64` | `int64` | Calendar day of month (1 to 31). |
| `Month` | `int64` | `int64` | Calendar month number (1 to 12). |
| `Year` | `int64` | `int64` | Transaction fiscal year (2021, 2022, 2023, 2024). |
| `Day Name` | `object` | `object` | Full standardized weekday name (Monday to Sunday). |
| `Brand` | `object` | `object` | Smartphone brand (Apple, Samsung, OnePlus, Vivo, Xiaomi). |
| `Mobile Model` | `object` | `object` | Specific phone model name (15 unique models). |
| `Units Sold` | `int64` | `int64` | Physical quantity purchased in the order (1 to 9). |
| `Price Per Unit` | `float64` | `float64` | Unit retail price in Indian Rupees (₹). |
| `Revenue` | *Derived* | `float64` | Total sales order amount: $\text{Units Sold} \times \text{Price Per Unit}$. |
| `Customer Name` | `object` | `object` | Customer name (988 unique customers). |
| `Customer Age` | `int64` | `int64` | Customer age in years (18 to 60). |
| `Age Group` | *Derived* | `category` | Segmented bracket (`< 25`, `25-34`, `35-49`, `50+`). |
| `City` | `object` | `object` | Retail store location (19 metropolitan cities). |
| `Payment Method` | `object` | `object` | Gateway channel (`UPI`, `Credit Card`, `Debit Card`, `Cash`). |
| `Customer Ratings`| `int64` | `int64` | Customer satisfaction score from 1 (lowest) to 5 (highest). |

---

## 5. Mathematical Formulations & Analytical Metrics

1. **Total Sales Revenue:**
   $$\text{Revenue} = \sum_{i=1}^{N} (\text{Units Sold}_i \times \text{Price Per Unit}_i)$$

2. **Average Selling Price (ASP):**
   $$\text{ASP} = \frac{1}{N} \sum_{i=1}^{N} \text{Price Per Unit}_i$$

3. **Average Transaction Value (ATV):**
   $$\text{ATV} = \frac{\text{Total Revenue}}{\text{Total Transactions}}$$

4. **Brand Market Revenue Share:**
   $$\text{Market Share}_{\text{Brand}} = \left( \frac{\text{Revenue}_{\text{Brand}}}{\text{Total Revenue}} \right) \times 100\%$$

5. **Year-over-Year (YoY) Growth Rate:**
   $$\text{YoY Growth}_t = \left( \frac{\text{Revenue}_t - \text{Revenue}_{t-1}}{\text{Revenue}_{t-1}} \right) \times 100\%$$

---

## 6. Empirical Findings & Actual Data Insights

From executing the Python and PySpark analytical pipelines across the complete 3,835 verified transactions:

1. **Macroeconomic Highlights:**
   - **Total Sales Revenue:** ₹769,204,987.97 (~₹769.20 Million / ₹76.92 Crore).
   - **Total Units Sold:** 19,150 units.
   - **Total Transactions:** 3,835 orders.
   - **Average Unit Price (ASP):** ₹40,114.04 per device.
   - **Average Transaction Value:** ₹200,574.96 per checkout.
   - **Mean Customer Satisfaction:** 3.69 / 5.00 stars.

2. **Brand & Model Dynamics:**
   - **Apple** is the revenue leader generating **₹161.62M** (21.01% revenue share) across 3,932 units sold.
   - **Samsung** closely follows with **₹160.04M** (20.81% revenue share) across 3,923 units sold.
   - **OnePlus** achieved **₹153.72M** (19.98% share), **Vivo** achieved **₹150.08M** (19.51% share), and **Xiaomi** generated **₹143.75M** (18.69% share).
   - The dataset shows a balanced, highly competitive distribution across all 5 smartphone brands, with Apple and Samsung commanding the premium price bracket.

3. **Payment Gateway Distribution:**
   - **UPI** and **Credit Card** represent the primary checkout gateways, contributing over 60% of total transactional volume, reflecting strong adoption of digital banking mechanisms in urban retail centers.

4. **Geographic Concentrations:**
   - Metropolitan tier-1 cities (**Delhi**, **Mumbai**, **Bengaluru**, **Kolkata**, **Chennai**) constitute the top revenue-generating clusters.

5. **Customer Demographics:**
   - Consumers in the **35–49 (Mid-Age)** and **25–34 (Young Adults)** age brackets generate over 70% of total revenue.
   - Higher-priced flagship models maintain consistent satisfaction ratings averaging ~3.7 to 4.2 stars.

---

## 7. Comparative Analysis: In-Memory Pandas vs. Distributed PySpark

| Dimension | Pandas Pipeline (`src/sales_analytics.py`) | Apache Spark Pipeline (`src/spark_analytics.py`) |
| :--- | :--- | :--- |
| **Processing Paradigm** | Single-node in-memory execution. | Distributed cluster computing across master/worker nodes. |
| **Execution Strategy** | Eager evaluation; operations execute immediately. | Lazy evaluation; builds Directed Acyclic Graph (DAG) until action invoked. |
| **Query Optimization** | Imperative Python vectorized execution. | Declarative optimization via Spark Catalyst Optimizer & Tungsten engine. |
| **Memory Constraint** | Restricted to available workstation RAM. | Partitioned data distribution with disk-spill support for out-of-core operations. |
| **Optimal Data Scale** | Ideal for datasets up to ~5–10 GB. | Ideal for enterprise datasets exceeding 100 GB to Petabyte scale. |

---

## 8. Conclusion and Future Scope

### 8.1 Conclusion
The project successfully converted the static Power BI Mobile Sales dashboard into an interactive, reproducible Python Big Data Analytics solution. The analytical results perfectly mirror the original business metrics (₹769.20M revenue, ~19k units sold, ~₹40.11k ASP) while adding programmatic rigor, distributed computing demonstrations via PySpark, and an interactive Streamlit UI.

### 8.2 Future Scope
1. **Real-Time Stream Processing:** Integrate an Apache Kafka producer simulation to stream real-time mobile order checkouts into Spark Structured Streaming.
2. **Predictive Machine Learning:** Build demand forecasting models (ARIMA/Prophet) to forecast monthly inventory requirements by city and brand.
3. **Cloud Lakehouse Deployment:** Deploy the pipeline on Databricks or AWS EMR using Delta Lake architecture with automated BI reporting.
