"""
app.py
------
Mobile Sales Analytics - Interactive Big Data Analytics Dashboard.
Built with Streamlit, Plotly, Pandas, and PySpark.
"""

import os
import sys
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Add src to system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.data_preprocessing import load_raw_data, clean_and_transform_data
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

# Page Configuration
st.set_page_config(
    page_title="Mobile Sales Analytics | Big Data Platform",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .metric-subtitle {
        color: #38bdf8;
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 4px;
    }
    
    /* Insight Banner */
    .insight-box {
        background-color: #0f2744;
        border-left: 5px solid #38bdf8;
        border-radius: 6px;
        padding: 14px 18px;
        margin: 15px 0;
        color: #e2e8f0;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 2px solid #334155;
        padding-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_clean_dataset() -> pd.DataFrame:
    """Load and clean dataset with caching for performance."""
    processed_path = "data/processed/mobile_sales_cleaned.csv"
    if os.path.exists(processed_path):
        df = pd.read_csv(processed_path)
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    else:
        raw_df = load_raw_data()
        df = clean_and_transform_data(raw_df)
        return df


def format_currency_inr(val: float) -> str:
    """Format large numbers into Indian Crores (Cr) or Millions (M)."""
    if val >= 1e7:
        return f"₹{val / 1e7:.2f} Cr"
    elif val >= 1e5:
        return f"₹{val / 1e5:.2f} Lakh"
    else:
        return f"₹{val:,.2f}"


def format_compact_inr(val: float) -> str:
    """Format in Millions for clean card display."""
    return f"₹{val / 1e6:.2f} M"


# Load Dataset
try:
    df_master = get_clean_dataset()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ==========================================
# SIDEBAR CONTROLS & FILTERS
# ==========================================
st.sidebar.image("Mobile-Sales-Analytics-PowerBI/Logo Mobile sales Data.png" if os.path.exists("Mobile-Sales-Analytics-PowerBI/Logo Mobile sales Data.png") else "https://img.icons8.com/color/96/smartphone.png", width=70)
st.sidebar.title("Sales Filter Engine")
st.sidebar.caption("Filter records across multiple dimensions")

# 1. Date Range
min_date = df_master["Date"].min().date()
max_date = df_master["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Select start and end dates to filter transactions"
)

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# 2. Multi-Select Filters
all_brands = sorted(df_master["Brand"].dropna().unique().tolist())
selected_brands = st.sidebar.multiselect("Brand", options=all_brands, default=all_brands)

# Dynamic filter: Models based on selected brands
available_models = sorted(df_master[df_master["Brand"].isin(selected_brands)]["Mobile Model"].dropna().unique().tolist())
selected_models = st.sidebar.multiselect("Mobile Model", options=available_models, default=available_models)

all_cities = sorted(df_master["City"].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect("City", options=all_cities, default=all_cities)

all_payments = sorted(df_master["Payment Method"].dropna().unique().tolist())
selected_payments = st.sidebar.multiselect("Payment Method", options=all_payments, default=all_payments)

# Apply Filters
mask = (
    (df_master["Date"].dt.date >= start_date) &
    (df_master["Date"].dt.date <= end_date) &
    (df_master["Brand"].isin(selected_brands)) &
    (df_master["Mobile Model"].isin(selected_models)) &
    (df_master["City"].isin(selected_cities)) &
    (df_master["Payment Method"].isin(selected_payments))
)
filtered_df = df_master[mask].copy()

# Filter status badge in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Records Matched:** `{len(filtered_df):,}` / `{len(df_master):,}`")
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **Academic Note:**\nPowered by Pandas, Plotly & PySpark. Converted from Power BI for Big Data Analytics.")

# ==========================================
# MAIN DASHBOARD INTERFACE
# ==========================================
st.title("📱 Mobile Sales Analytics Platform")
st.markdown("##### *Big Data Analytics and Interactive Decision Support System*")

if filtered_df.empty:
    st.warning("⚠️ No records match the selected filter criteria. Please broaden your selection.")
    st.stop()

# Compute KPIs for filtered dataset
kpis = compute_kpis(filtered_df)

# Top KPI Metric Cards
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Revenue</div>
        <div class="metric-value">{format_compact_inr(kpis['total_revenue'])}</div>
        <div class="metric-subtitle">{format_currency_inr(kpis['total_revenue'])}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Units Sold</div>
        <div class="metric-value">{kpis['total_units']:,}</div>
        <div class="metric-subtitle">Across {kpis['total_transactions']:,} transactions</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Unit Price</div>
        <div class="metric-value">₹{kpis['avg_price_per_unit']/1000:.1f}k</div>
        <div class="metric-subtitle">₹{kpis['avg_price_per_unit']:,.2f} / unit</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Order Value</div>
        <div class="metric-value">₹{kpis['avg_transaction_value']/1000:.1f}k</div>
        <div class="metric-subtitle">Per transaction checkout</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Rating</div>
        <div class="metric-value">⭐ {kpis['avg_rating']:.2f} / 5</div>
        <div class="metric-subtitle">From {kpis['unique_customers']:,} customers</div>
    </div>
    """, unsafe_allow_html=True)

# Navigation Tabs
tabs = st.tabs([
    "📊 Executive Summary",
    "📱 Brand & Model Performance",
    "📈 Time Trends & YoY",
    "🏙️ Geographic & Payments",
    "👥 Customer Analytics",
    "⚡ Big Data & PySpark",
    "🔍 Data Explorer & Export"
])

# -------------------------------------------------------------
# TAB 1: EXECUTIVE SUMMARY
# -------------------------------------------------------------
with tabs[0]:
    st.markdown('<div class="section-header">Executive Performance Highlights</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        # Monthly Revenue Trend Plotly Chart
        monthly_df = compute_monthly_trends(filtered_df)
        fig_trend = px.area(
            monthly_df,
            x="Year-Month",
            y="Revenue",
            title="Monthly Sales Revenue Trajectory (INR)",
            labels={"Revenue": "Total Revenue (₹)", "Year-Month": "Month"},
            color_discrete_sequence=["#38bdf8"]
        )
        fig_trend.update_layout(
            hovermode="x unified",
            margin=dict(l=20, r=20, t=40, b=20),
            template="plotly_dark",
            yaxis_tickprefix="₹"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        # Brand Market Share Donut Chart
        brand_df = compute_brand_metrics(filtered_df)
        fig_brand_pie = px.pie(
            brand_df,
            names="Brand",
            values="Revenue",
            title="Revenue Share by Brand",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_brand_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_brand_pie.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            template="plotly_dark"
        )
        st.plotly_chart(fig_brand_pie, use_container_width=True)

    # Dynamic Analytical Insights Box
    st.markdown(f"""
    <div class="insight-box">
        <h4>📌 Real Empirical Findings & Key Insights:</h4>
        <ul>
            <li><strong>Market Leaders:</strong> <code>{kpis['top_brand']}</code> commands the largest revenue contribution with 
            competitive positioning from Samsung and OnePlus.</li>
            <li><strong>Geographic Hub:</strong> <code>{kpis['top_city']}</code> represents the highest revenue-generating metropolitan market.</li>
            <li><strong>Payment Dominance:</strong> <code>{kpis['top_payment_method']}</code> is the most popular transaction gateway among buyers.</li>
            <li><strong>Average Basket Size:</strong> Buyers average <strong>~5 units</strong> per transaction at an average unit price of <strong>₹{kpis['avg_price_per_unit']:,.2f}</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 2: BRAND & MODEL PERFORMANCE
# -------------------------------------------------------------
with tabs[1]:
    st.markdown('<div class="section-header">Brand and Model Comparative Analysis</div>', unsafe_allow_html=True)
    
    b_col1, b_col2 = st.columns(2)
    
    with b_col1:
        brand_df = compute_brand_metrics(filtered_df)
        fig_brand_bar = px.bar(
            brand_df,
            x="Brand",
            y="Revenue",
            color="Units_Sold",
            text="Revenue_Share_Pct",
            title="Brand-Wise Revenue & Units Sold",
            labels={"Revenue": "Total Revenue (₹)", "Units_Sold": "Units Sold", "Revenue_Share_Pct": "Share %"},
            color_continuous_scale="Teal"
        )
        fig_brand_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_brand_bar.update_layout(template="plotly_dark", yaxis_tickprefix="₹")
        st.plotly_chart(fig_brand_bar, use_container_width=True)

    with b_col2:
        model_df = compute_model_metrics(filtered_df, top_n=10)
        fig_model = px.bar(
            model_df,
            x="Revenue",
            y="Mobile Model",
            color="Brand",
            orientation="h",
            title="Top 10 Mobile Models by Revenue",
            labels={"Revenue": "Total Revenue (₹)", "Mobile Model": "Model"},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_model.update_layout(template="plotly_dark", yaxis={'categoryorder': 'total ascending'}, xaxis_tickprefix="₹")
        st.plotly_chart(fig_model, use_container_width=True)

    # Detailed Brand & Model Data Table
    st.subheader("Model-Level Performance Matrix")
    all_models_df = compute_model_metrics(filtered_df, top_n=50)
    st.dataframe(
        all_models_df.style.format({
            "Revenue": "₹{:,.2f}",
            "Avg_Price": "₹{:,.2f}",
            "Units_Sold": "{:,}",
            "Transactions": "{:,}",
            "Avg_Rating": "{:.2f}",
            "Revenue_Share_Pct": "{:.2f}%"
        }),
        use_container_width=True
    )

# -------------------------------------------------------------
# TAB 3: TIME TRENDS & YOY
# -------------------------------------------------------------
with tabs[2]:
    st.markdown('<div class="section-header">Time Series Trends & Year-over-Year (YoY) Dynamics</div>', unsafe_allow_html=True)
    
    yoy_df = compute_yoy_metrics(filtered_df)
    
    y_col1, y_col2 = st.columns([1, 2])
    
    with y_col1:
        st.subheader("Yearly Growth Summary")
        st.dataframe(
            yoy_df.style.format({
                "Revenue": "₹{:,.2f}",
                "Units_Sold": "{:,}",
                "Transactions": "{:,}",
                "Avg_Price": "₹{:,.2f}",
                "YoY_Revenue_Growth_Pct": "{:+.2f}%",
                "YoY_Units_Growth_Pct": "{:+.2f}%"
            }),
            use_container_width=True
        )
        
    with y_col2:
        fig_yoy = px.bar(
            yoy_df,
            x="Year",
            y="Revenue",
            text="Revenue",
            title="Annual Revenue Trajectory",
            color="Year",
            color_continuous_scale="Viridis"
        )
        fig_yoy.update_traces(texttemplate="₹%{text:.2s}", textposition="outside")
        fig_yoy.update_layout(template="plotly_dark", yaxis_tickprefix="₹")
        st.plotly_chart(fig_yoy, use_container_width=True)

    # Day of Week & Quarterly Performance
    st.subheader("Seasonal & Day-of-Week Patterns")
    d_col1, d_col2 = st.columns(2)
    
    with d_col1:
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_df = filtered_df.groupby("Day Name")["Revenue"].agg(["sum", "count"]).reindex(dow_order).reset_index()
        fig_dow = px.bar(
            dow_df,
            x="Day Name",
            y="sum",
            title="Revenue Distribution by Day of Week",
            labels={"sum": "Total Revenue (₹)", "Day Name": "Day"},
            color="sum",
            color_continuous_scale="Purples"
        )
        fig_dow.update_layout(template="plotly_dark", yaxis_tickprefix="₹")
        st.plotly_chart(fig_dow, use_container_width=True)
        
    with d_col2:
        quarter_df = filtered_df.groupby("Year-Quarter")["Revenue"].sum().reset_index()
        fig_q = px.line(
            quarter_df,
            x="Year-Quarter",
            y="Revenue",
            markers=True,
            title="Quarterly Sales Evolution",
            labels={"Revenue": "Total Revenue (₹)", "Year-Quarter": "Quarter"},
            color_discrete_sequence=["#e879f9"]
        )
        fig_q.update_layout(template="plotly_dark", yaxis_tickprefix="₹")
        st.plotly_chart(fig_q, use_container_width=True)

# -------------------------------------------------------------
# TAB 4: GEOGRAPHIC & PAYMENTS
# -------------------------------------------------------------
with tabs[3]:
    st.markdown('<div class="section-header">Geographic Reach and Payment Methods</div>', unsafe_allow_html=True)
    
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        city_df = compute_city_metrics(filtered_df).head(12)
        fig_city = px.bar(
            city_df,
            x="Revenue",
            y="City",
            orientation="h",
            title="Top 12 Cities by Revenue",
            labels={"Revenue": "Total Revenue (₹)", "City": "City"},
            color="Revenue",
            color_continuous_scale="Blues"
        )
        fig_city.update_layout(template="plotly_dark", yaxis={'categoryorder': 'total ascending'}, xaxis_tickprefix="₹")
        st.plotly_chart(fig_city, use_container_width=True)
        
    with g_col2:
        pay_df = compute_payment_metrics(filtered_df)
        fig_pay = px.pie(
            pay_df,
            names="Payment Method",
            values="Transactions",
            title="Transaction Volume by Payment Gateway",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_pay.update_traces(textposition="inside", textinfo="percent+label")
        fig_pay.update_layout(template="plotly_dark")
        st.plotly_chart(fig_pay, use_container_width=True)

    # City vs Brand Cross-Tabulation
    st.subheader("City vs. Brand Revenue Heatmap")
    top_cities_list = compute_city_metrics(filtered_df).head(8)["City"].tolist()
    pivot_cb = filtered_df[filtered_df["City"].isin(top_cities_list)].pivot_table(
        index="City",
        columns="Brand",
        values="Revenue",
        aggfunc="sum",
        fill_value=0
    )
    fig_heat = px.imshow(
        pivot_cb / 1e6,
        labels=dict(x="Brand", y="City", color="Revenue (₹ Millions)"),
        x=pivot_cb.columns,
        y=pivot_cb.index,
        color_continuous_scale="Viridis",
        title="Revenue Matrix (₹ Millions) Across Top Cities and Brands"
    )
    fig_heat.update_layout(template="plotly_dark")
    st.plotly_chart(fig_heat, use_container_width=True)

# -------------------------------------------------------------
# TAB 5: CUSTOMER ANALYTICS
# -------------------------------------------------------------
with tabs[4]:
    st.markdown('<div class="section-header">Customer Demographics and Satisfaction Metrics</div>', unsafe_allow_html=True)
    
    demo_dict = compute_customer_demographics(filtered_df)
    
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        fig_age = px.bar(
            demo_dict["age_groups"],
            x="Age Group",
            y="Revenue",
            color="Avg_Spend",
            title="Revenue Contribution by Customer Age Bracket",
            labels={"Revenue": "Total Revenue (₹)", "Age Group": "Demographic Bracket", "Avg_Spend": "Avg Spend (₹)"},
            color_continuous_scale="Sunset"
        )
        fig_age.update_layout(template="plotly_dark", yaxis_tickprefix="₹")
        st.plotly_chart(fig_age, use_container_width=True)
        
    with c_col2:
        fig_rating = px.bar(
            demo_dict["ratings"],
            x="Customer Ratings",
            y="Count",
            text="Share_Pct",
            title="Customer Rating Distribution (1 to 5 Stars)",
            labels={"Customer Ratings": "Rating", "Count": "Number of Transactions", "Share_Pct": "Share %"},
            color="Customer Ratings",
            color_continuous_scale="Oranges"
        )
        fig_rating.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_rating.update_layout(template="plotly_dark")
        st.plotly_chart(fig_rating, use_container_width=True)

    # Boxplot of Price by Rating
    fig_box = px.box(
        filtered_df,
        x="Customer Ratings",
        y="Price Per Unit",
        color="Brand",
        title="Unit Price Spread Across Customer Rating Categories",
        labels={"Price Per Unit": "Price Per Unit (₹)", "Customer Ratings": "Rating"}
    )
    fig_box.update_layout(template="plotly_dark", yaxis_tickprefix="₹")
    st.plotly_chart(fig_box, use_container_width=True)

# -------------------------------------------------------------
# TAB 6: BIG DATA & PYSPARK ENGINE
# -------------------------------------------------------------
with tabs[5]:
    st.markdown('<div class="section-header">Big Data Architecture & The Five Vs Framework</div>', unsafe_allow_html=True)
    
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.markdown("""
        ### 🌐 The Five Vs of Big Data Analysis
        
        * **1. Volume (Dataset Scale):**
          * *Current State:* 3,835 records (~480 KB CSV). This dataset fits easily in RAM and is ideal for prototyping and academic experimentation.
          * *Production Scale:* In an enterprise telecom/e-commerce setting (e.g. Amazon, Flipkart), transaction velocity generates millions of records daily, requiring distributed cluster storage (HDFS, Amazon S3, Azure Data Lake).
          
        * **2. Velocity (Data Arrival Rate):**
          * *Current State:* Historical transactional batch data spanning 2021 to 2024.
          * *Production Scale:* Streaming pipelines using Apache Kafka or Spark Structured Streaming would ingest real-time POS checkouts and flash-sale spikes.
          
        * **3. Variety (Data Types & Structures):**
          * *Current State:* Structured tabular transactional schema (numerical, temporal, categorical fields).
          * *Production Scale:* Semi-structured JSON clickstreams, unstructured customer reviews, social media sentiment, and image specs.
        """)
        
    with v_col2:
        st.markdown("""
        ### 🔍 Veracity & Value Framework
        
        * **4. Veracity (Data Quality & Trustworthiness):**
          * *Data Audit:* No missing null records; verified positive numeric ranges for price and units sold.
          * *Normalization:* Resolved inconsistent day-name entries (`Sat` vs `Saturday`) via deterministic datetime casting.
          
        * **5. Value (Actionable Business Return):**
          * Dynamic pricing optimization by model elasticity.
          * Inventory replenishment tailored to city-level brand affinities.
          * Payment gateway fee mitigation (promoting low-fee UPI over credit cards).
        """)

    st.markdown("---")
    st.subheader("⚡ Distributed Computing Demonstration with Apache Spark")
    st.caption("Execute PySpark DataFrame transformations and Spark SQL in real-time.")

    if st.button("🚀 Run Distributed Spark Aggregations"):
        with st.spinner("Initializing PySpark session and executing distributed queries..."):
            try:
                from src.spark_analytics import run_spark_analysis
                spark_res = run_spark_analysis()
                if spark_res.get("status") == "success":
                    st.success(f"✅ Spark {spark_res['spark_version']} executed successfully across {spark_res['partitions']} partition(s)!")
                    s_c1, s_c2 = st.columns(2)
                    with s_c1:
                        st.markdown("**Spark SQL Brand Aggregations:**")
                        st.dataframe(spark_res["brand_summary"], use_container_width=True)
                    with s_c2:
                        st.markdown("**PySpark DataFrame Payment Summary:**")
                        st.dataframe(spark_res["payment_summary"], use_container_width=True)
                else:
                    st.warning(f"Spark Notice: {spark_res.get('message')}")
            except Exception as e:
                st.error(f"PySpark execution notice: {e}")

# -------------------------------------------------------------
# TAB 7: DATA EXPLORER & EXPORT
# -------------------------------------------------------------
with tabs[6]:
    st.markdown('<div class="section-header">Raw & Filtered Sales Records Explorer</div>', unsafe_allow_html=True)
    
    col_search, col_cols = st.columns([2, 3])
    with col_search:
        search_query = st.text_input("🔍 Search customer name, model, or city:")
    with col_cols:
        all_display_cols = list(filtered_df.columns)
        default_cols = ["Transaction ID", "Date", "Brand", "Mobile Model", "Units Sold", "Price Per Unit", "Revenue", "City", "Payment Method", "Customer Ratings"]
        selected_cols = st.multiselect("Visible Columns", options=all_display_cols, default=default_cols)

    display_df = filtered_df[selected_cols]
    if search_query:
        search_mask = (
            filtered_df["Customer Name"].str.contains(search_query, case=False, na=False) |
            filtered_df["Mobile Model"].str.contains(search_query, case=False, na=False) |
            filtered_df["City"].str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[search_mask]

    st.dataframe(display_df, use_container_width=True, height=450)
    
    # Download buttons
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name=f"mobile_sales_filtered_{datetime.date.today()}.csv",
        mime="text/csv",
        help="Export current filtered view to CSV file"
    )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
    "Big Data Analytics Project | Converted from Power BI Mobile Sales Analytics | Python, Streamlit, Plotly & PySpark"
    "</div>",
    unsafe_allow_html=True
)
