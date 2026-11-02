"""
sales_analytics.py
------------------
Module containing business logic, statistical analytics, KPI aggregations,
time-series trend evaluations, and chart generation utilities for Mobile Sales Analytics.
"""

import os
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless figure generation
import matplotlib.pyplot as plt
import seaborn as sns


def compute_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute core headline KPIs from the given mobile sales DataFrame.
    """
    if df.empty:
        return {
            "total_revenue": 0.0,
            "total_units": 0,
            "total_transactions": 0,
            "avg_price_per_unit": 0.0,
            "avg_rating": 0.0,
            "avg_transaction_value": 0.0,
            "unique_customers": 0,
            "top_brand": "N/A",
            "top_city": "N/A",
            "top_payment_method": "N/A"
        }

    total_revenue = float(df["Revenue"].sum())
    total_units = int(df["Units Sold"].sum())
    total_transactions = int(len(df))
    avg_price_per_unit = float(df["Price Per Unit"].mean())
    avg_rating = float(df["Customer Ratings"].mean())
    avg_transaction_value = float(total_revenue / total_transactions) if total_transactions > 0 else 0.0
    unique_customers = int(df["Customer Name"].nunique()) if "Customer Name" in df.columns else 0

    brand_rev = df.groupby("Brand")["Revenue"].sum()
    top_brand = brand_rev.idxmax() if not brand_rev.empty else "N/A"

    city_rev = df.groupby("City")["Revenue"].sum()
    top_city = city_rev.idxmax() if not city_rev.empty else "N/A"

    payment_counts = df["Payment Method"].value_counts()
    top_payment_method = payment_counts.idxmax() if not payment_counts.empty else "N/A"

    return {
        "total_revenue": round(total_revenue, 2),
        "total_units": total_units,
        "total_transactions": total_transactions,
        "avg_price_per_unit": round(avg_price_per_unit, 2),
        "avg_rating": round(avg_rating, 2),
        "avg_transaction_value": round(avg_transaction_value, 2),
        "unique_customers": unique_customers,
        "top_brand": top_brand,
        "top_city": top_city,
        "top_payment_method": top_payment_method
    }


def compute_brand_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate sales metrics grouped by Brand:
    Revenue, Units Sold, Transactions, Avg Price, Avg Rating, Revenue Share %.
    """
    if df.empty:
        return pd.DataFrame()

    total_revenue = df["Revenue"].sum()
    grouped = df.groupby("Brand").agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units Sold", "sum"),
        Transactions=("Transaction ID", "count"),
        Avg_Price=("Price Per Unit", "mean"),
        Avg_Rating=("Customer Ratings", "mean")
    ).reset_index()

    grouped["Revenue_Share_Pct"] = ((grouped["Revenue"] / total_revenue) * 100).round(2)
    grouped["Revenue"] = grouped["Revenue"].round(2)
    grouped["Avg_Price"] = grouped["Avg_Price"].round(2)
    grouped["Avg_Rating"] = grouped["Avg_Rating"].round(2)
    return grouped.sort_values(by="Revenue", ascending=False).reset_index(drop=True)


def compute_model_metrics(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """
    Aggregate metrics grouped by Mobile Model (and associated Brand).
    """
    if df.empty:
        return pd.DataFrame()

    total_revenue = df["Revenue"].sum()
    grouped = df.groupby(["Brand", "Mobile Model"]).agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units Sold", "sum"),
        Transactions=("Transaction ID", "count"),
        Avg_Price=("Price Per Unit", "mean"),
        Avg_Rating=("Customer Ratings", "mean")
    ).reset_index()

    grouped["Revenue_Share_Pct"] = ((grouped["Revenue"] / total_revenue) * 100).round(2)
    grouped["Revenue"] = grouped["Revenue"].round(2)
    grouped["Avg_Price"] = grouped["Avg_Price"].round(2)
    grouped["Avg_Rating"] = grouped["Avg_Rating"].round(2)
    return grouped.sort_values(by="Revenue", ascending=False).head(top_n).reset_index(drop=True)


def compute_city_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate sales performance metrics by City.
    """
    if df.empty:
        return pd.DataFrame()

    total_revenue = df["Revenue"].sum()
    grouped = df.groupby("City").agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units Sold", "sum"),
        Transactions=("Transaction ID", "count"),
        Avg_Rating=("Customer Ratings", "mean")
    ).reset_index()

    grouped["Revenue_Share_Pct"] = ((grouped["Revenue"] / total_revenue) * 100).round(2)
    grouped["Revenue"] = grouped["Revenue"].round(2)
    grouped["Avg_Rating"] = grouped["Avg_Rating"].round(2)
    return grouped.sort_values(by="Revenue", ascending=False).reset_index(drop=True)


def compute_payment_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate transactions, revenue, and unit count by Payment Method.
    """
    if df.empty:
        return pd.DataFrame()

    total_rev = df["Revenue"].sum()
    total_tx = len(df)
    grouped = df.groupby("Payment Method").agg(
        Transactions=("Transaction ID", "count"),
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units Sold", "sum"),
        Avg_Transaction_Val=("Revenue", "mean")
    ).reset_index()

    grouped["Tx_Share_Pct"] = ((grouped["Transactions"] / total_tx) * 100).round(2)
    grouped["Revenue_Share_Pct"] = ((grouped["Revenue"] / total_rev) * 100).round(2)
    grouped["Revenue"] = grouped["Revenue"].round(2)
    grouped["Avg_Transaction_Val"] = grouped["Avg_Transaction_Val"].round(2)
    return grouped.sort_values(by="Revenue", ascending=False).reset_index(drop=True)


def compute_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate monthly sales time series:
    Revenue, Units Sold, Transaction Count, YoY growth where comparable.
    """
    if df.empty:
        return pd.DataFrame()

    grouped = df.groupby(["Year", "Month", "Year-Month"]).agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units Sold", "sum"),
        Transactions=("Transaction ID", "count"),
        Avg_Price=("Price Per Unit", "mean")
    ).reset_index().sort_values(by=["Year", "Month"])

    grouped["Revenue"] = grouped["Revenue"].round(2)
    grouped["Avg_Price"] = grouped["Avg_Price"].round(2)

    # Calculate MoM (Month-over-Month) percentage change
    grouped["MoM_Revenue_Growth_Pct"] = grouped["Revenue"].pct_change().multiply(100).round(2)
    return grouped.reset_index(drop=True)


def compute_yoy_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Year-over-Year (YoY) total revenue and unit metrics across fiscal/calendar years.
    """
    if df.empty:
        return pd.DataFrame()

    yearly = df.groupby("Year").agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units Sold", "sum"),
        Transactions=("Transaction ID", "count"),
        Avg_Price=("Price Per Unit", "mean")
    ).reset_index().sort_values(by="Year")

    yearly["YoY_Revenue_Growth_Pct"] = yearly["Revenue"].pct_change().multiply(100).round(2)
    yearly["YoY_Units_Growth_Pct"] = yearly["Units_Sold"].pct_change().multiply(100).round(2)
    yearly["Revenue"] = yearly["Revenue"].round(2)
    yearly["Avg_Price"] = yearly["Avg_Price"].round(2)
    return yearly.reset_index(drop=True)


def compute_customer_demographics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute customer age group statistics, ratings breakdown, and spending patterns.
    """
    if df.empty:
        return {"age_groups": pd.DataFrame(), "ratings": pd.DataFrame()}

    age_grouped = df.groupby("Age Group", observed=False).agg(
        Transactions=("Transaction ID", "count"),
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units Sold", "sum"),
        Avg_Rating=("Customer Ratings", "mean"),
        Avg_Spend=("Revenue", "mean")
    ).reset_index()
    age_grouped["Revenue"] = age_grouped["Revenue"].round(2)
    age_grouped["Avg_Spend"] = age_grouped["Avg_Spend"].round(2)
    age_grouped["Avg_Rating"] = age_grouped["Avg_Rating"].round(2)

    rating_grouped = df.groupby("Customer Ratings").agg(
        Count=("Transaction ID", "count"),
        Revenue=("Revenue", "sum")
    ).reset_index()
    rating_grouped["Share_Pct"] = ((rating_grouped["Count"] / len(df)) * 100).round(2)

    return {
        "age_groups": age_grouped,
        "ratings": rating_grouped
    }


def generate_static_visualizations(df: pd.DataFrame, output_dir: str = "outputs/figures") -> List[str]:
    """
    Generate publication-grade statistical charts using Matplotlib and Seaborn,
    saving them as high-resolution PNG images.
    """
    os.makedirs(output_dir, exist_ok=True)
    generated_files = []
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams["font.family"] = "sans-serif"

    # 1. Brand Revenue & Unit Comparison Chart
    fig, ax1 = plt.subplots(figsize=(10, 6))
    brand_df = compute_brand_metrics(df)
    x = np.arange(len(brand_df))
    width = 0.38

    ax1.bar(x - width/2, brand_df["Revenue"] / 1e6, width, label="Revenue (INR Millions)", color="#1f77b4", alpha=0.9)
    ax2 = ax1.twinx()
    ax2.bar(x + width/2, brand_df["Units_Sold"], width, label="Units Sold", color="#ff7f0e", alpha=0.9)

    ax1.set_xlabel("Brand", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Revenue (INR Millions)", fontsize=12, color="#1f77b4")
    ax2.set_ylabel("Units Sold", fontsize=12, color="#ff7f0e")
    ax1.set_xticks(x)
    ax1.set_xticklabels(brand_df["Brand"], fontsize=11)
    ax1.set_title("Brand-Wise Revenue and Units Sold Comparison", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()

    out1 = os.path.join(output_dir, "brand_revenue_distribution.png")
    fig.savefig(out1, dpi=300)
    plt.close(fig)
    generated_files.append(out1)

    # 2. Monthly Revenue Trend Chart
    monthly_df = compute_monthly_trends(df)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_df["Year-Month"], monthly_df["Revenue"] / 1e6, marker="o", linewidth=2.5, color="#2ca02c")
    ax.set_title("Monthly Sales Revenue Trend (2021 - 2024)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Year-Month", fontsize=12)
    ax.set_ylabel("Revenue (INR Millions)", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    fig.tight_layout()

    out2 = os.path.join(output_dir, "monthly_sales_trend.png")
    fig.savefig(out2, dpi=300)
    plt.close(fig)
    generated_files.append(out2)

    # 3. Top Cities Revenue Chart
    city_df = compute_city_metrics(df).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=city_df, x="Revenue", y="City", ax=ax, hue="City", palette="Blues_r", legend=False)
    ax.set_title("Top 10 Cities by Total Revenue", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Revenue (INR)", fontsize=12)
    ax.set_ylabel("City", fontsize=12)
    for p in ax.patches:
        val = p.get_width()
        ax.annotate(f"INR {val/1e6:.1f}M", (val, p.get_y() + p.get_height() / 2.),
                    ha="left", va="center", xytext=(5, 0), textcoords="offset points", fontsize=9)
    fig.tight_layout()

    out3 = os.path.join(output_dir, "city_sales_comparison.png")
    fig.savefig(out3, dpi=300)
    plt.close(fig)
    generated_files.append(out3)

    # 4. Payment Method Share Donut / Pie
    pay_df = compute_payment_metrics(df)
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#4e79a7", "#f28e2c", "#e15759", "#76b7b2"]
    ax.pie(
        pay_df["Revenue"],
        labels=pay_df["Payment Method"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.4, edgecolor="w")
    )
    ax.set_title("Payment Method Distribution by Revenue", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()

    out4 = os.path.join(output_dir, "payment_method_breakdown.png")
    fig.savefig(out4, dpi=300)
    plt.close(fig)
    generated_files.append(out4)

    # 5. Customer Age Distribution & Ratings Heatmap/Boxplot
    fig, (ax_box, ax_hist) = plt.subplots(1, 2, figsize=(14, 6))
    sns.boxplot(data=df, x="Customer Ratings", y="Price Per Unit", ax=ax_box, hue="Customer Ratings", palette="Purples", legend=False)
    ax_box.set_title("Price Distribution Across Customer Ratings", fontsize=12, fontweight="bold")
    ax_box.set_xlabel("Customer Rating (1 to 5)", fontsize=11)
    ax_box.set_ylabel("Price Per Unit (INR)", fontsize=11)

    sns.histplot(df["Customer Age"], bins=15, kde=True, ax=ax_hist, color="#9467bd")
    ax_hist.set_title("Customer Age Demographic Distribution", fontsize=12, fontweight="bold")
    ax_hist.set_xlabel("Customer Age", fontsize=11)
    ax_hist.set_ylabel("Count", fontsize=11)

    fig.tight_layout()
    out5 = os.path.join(output_dir, "customer_age_ratings_distribution.png")
    fig.savefig(out5, dpi=300)
    plt.close(fig)
    generated_files.append(out5)

    return generated_files


if __name__ == "__main__":
    from data_preprocessing import load_raw_data, clean_and_transform_data
    df = clean_and_transform_data(load_raw_data())
    kpis = compute_kpis(df)
    print("KPIs:", kpis)
    figs = generate_static_visualizations(df)
    print(f"Generated {len(figs)} static charts:", figs)
