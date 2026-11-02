"""
spark_analytics.py
------------------
PySpark implementation for Mobile Sales Analytics demonstrating distributed
computing concepts, DataFrame API operations, and Spark SQL queries for Big Data Analytics.
"""

import os
from typing import Dict, Any, Tuple
import pandas as pd


def get_spark_session(app_name: str = "MobileSalesBigDataAnalytics"):
    """
    Initialize and return a local SparkSession with suppressed verbosity.
    """
    try:
        from pyspark.sql import SparkSession
        spark = (
            SparkSession.builder
            .appName(app_name)
            .master("local[*]")
            .config("spark.driver.memory", "2g")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.ui.enabled", "false")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")
        return spark
    except Exception as e:
        print(f"[PySpark Warning] Could not initialize SparkSession: {e}")
        return None


def run_spark_analysis(csv_path: str = "data/processed/mobile_sales_cleaned.csv") -> Dict[str, Any]:
    """
    Execute big data analytics workflow using PySpark DataFrame API and Spark SQL:
    1. Ingest cleaned CSV into distributed PySpark DataFrame.
    2. Validate schema and partition count.
    3. Compute distributed aggregations (Brand, City, Payment Method).
    4. Execute Spark SQL queries on temporary view.
    5. Return analytical results as standard pandas DataFrames for downstream consumption.
    """
    if not os.path.exists(csv_path):
        csv_path = "data/raw/mobile_sales_data.csv"
        if not os.path.exists(csv_path):
            csv_path = "Mobile-Sales-Analytics-PowerBI/Mobile Sales Data.csv"

    spark = get_spark_session()
    if spark is None:
        return {"status": "unavailable", "message": "PySpark or Java not configured properly."}

    from pyspark.sql.functions import col, sum as _sum, avg as _avg, count as _count, round as _round

    # 1. Ingest dataset
    sdf = spark.read.csv(csv_path, header=True, inferSchema=True)

    # Ensure Revenue column exists
    if "Revenue" not in sdf.columns:
        sdf = sdf.withColumn("Revenue", _round(col("Units Sold") * col("Price Per Unit"), 2))

    # Register temporary view for Spark SQL queries
    sdf.createOrReplaceTempView("mobile_sales_view")

    # 2. Overall KPI Aggregations using PySpark DataFrame API
    kpi_df = sdf.agg(
        _round(_sum("Revenue"), 2).alias("total_revenue"),
        _sum("Units Sold").alias("total_units"),
        _count("Transaction ID").alias("total_transactions"),
        _round(_avg("Price Per Unit"), 2).alias("avg_price_per_unit"),
        _round(_avg("Customer Ratings"), 2).alias("avg_rating")
    ).toPandas()

    kpi_dict = kpi_df.to_dict(orient="records")[0]

    # 3. Brand Analytics via Spark SQL
    brand_sql = """
        SELECT 
            Brand,
            ROUND(SUM(Revenue), 2) AS Total_Revenue,
            SUM(`Units Sold`) AS Total_Units,
            COUNT(`Transaction ID`) AS Transaction_Count,
            ROUND(AVG(`Price Per Unit`), 2) AS Avg_Price
        FROM mobile_sales_view
        GROUP BY Brand
        ORDER BY Total_Revenue DESC
    """
    brand_df = spark.sql(brand_sql).toPandas()

    # 4. City Analytics via PySpark DataFrame API
    city_df = (
        sdf.groupBy("City")
        .agg(
            _round(_sum("Revenue"), 2).alias("Total_Revenue"),
            _sum("Units Sold").alias("Total_Units"),
            _count("Transaction ID").alias("Transactions")
        )
        .orderBy(col("Total_Revenue").desc())
        .toPandas()
    )

    # 5. Payment Method Analytics via Spark SQL
    pay_sql = """
        SELECT 
            `Payment Method` AS Payment_Method,
            COUNT(`Transaction ID`) AS Transactions,
            ROUND(SUM(Revenue), 2) AS Total_Revenue
        FROM mobile_sales_view
        GROUP BY `Payment Method`
        ORDER BY Total_Revenue DESC
    """
    payment_df = spark.sql(pay_sql).toPandas()

    partitions = sdf.rdd.getNumPartitions()

    return {
        "status": "success",
        "spark_version": spark.version,
        "partitions": partitions,
        "record_count": sdf.count(),
        "kpis": kpi_dict,
        "brand_summary": brand_df,
        "city_summary": city_df,
        "payment_summary": payment_df
    }


if __name__ == "__main__":
    results = run_spark_analysis()
    if results.get("status") == "success":
        print(f"PySpark {results['spark_version']} Analytics Completed Successfully!")
        print(f"Partitions: {results['partitions']}, Records: {results['record_count']}")
        print("KPIs:", results["kpis"])
        print("\nBrand Summary (Spark SQL):\n", results["brand_summary"])
    else:
        print("PySpark Execution Result:", results)
