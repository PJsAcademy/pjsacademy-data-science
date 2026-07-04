# ============================================================================
# PJ's Academy · Snowflake Project 17 — Streamlit in Snowflake  (Advanced)
# ----------------------------------------------------------------------------
# WHAT YOU BUILD: a live analytics dashboard running NATIVELY inside Snowflake
#   with Streamlit — no external hosting, data never leaves the platform.
# HOW TO RUN: Snowsight → Projects → Streamlit → "+ Streamlit App", paste this.
#   (Locally you'd need snowflake-connector; in-Snowflake it just works.)
# ============================================================================

import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="PJ's Academy — Live Dashboard", layout="wide")
session = get_active_session()   # provided automatically in Snowflake

st.title("❄️ Live Sales Dashboard — PJ's Academy")
st.caption("Runs inside Snowflake · data never leaves the platform")

# 0) One-time demo data (safe to re-run) ------------------------------------
session.sql("""
  CREATE TABLE IF NOT EXISTS sales_demo (
    region STRING, product STRING, order_date DATE, revenue NUMBER(12,2))
""").collect()
if session.table("sales_demo").count() == 0:
    session.sql("""INSERT INTO sales_demo VALUES
      ('South','Laptop','2023-06-01',55000),('North','Mouse','2023-06-02',1400),
      ('South','Desk','2023-06-03',8000),('West','Chair','2023-06-04',4500),
      ('North','Monitor','2023-06-05',15000),('South','Laptop','2023-06-06',55000)
    """).collect()

# 1) Sidebar filter ----------------------------------------------------------
regions = [r[0] for r in session.sql(
    "SELECT DISTINCT region FROM sales_demo ORDER BY 1").collect()]
picked = st.sidebar.multiselect("Regions", regions, default=regions)

# 2) Query (pushed down to Snowflake compute) -------------------------------
region_list = "','".join(picked) if picked else "___none___"
df = session.sql(f"""
    SELECT region, SUM(revenue) AS revenue, COUNT(*) AS orders
    FROM sales_demo
    WHERE region IN ('{region_list}')
    GROUP BY region ORDER BY revenue DESC
""").to_pandas()

# 3) KPIs --------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"₹{df['REVENUE'].sum():,.0f}")
c2.metric("Total Orders",  int(df['ORDERS'].sum()))
c3.metric("Regions",       len(df))

# 4) Charts ------------------------------------------------------------------
st.subheader("Revenue by Region")
st.bar_chart(df.set_index("REGION")["REVENUE"])

# 5) Time series -------------------------------------------------------------
ts = session.sql(f"""
    SELECT order_date, SUM(revenue) AS revenue
    FROM sales_demo WHERE region IN ('{region_list}')
    GROUP BY order_date ORDER BY order_date
""").to_pandas()
st.subheader("Daily Revenue Trend")
st.line_chart(ts.set_index("ORDER_DATE")["REVENUE"])

st.dataframe(df, use_container_width=True)

# ============================================================================
# LEARNED: Streamlit in Snowflake, get_active_session, running SQL from the app,
# to_pandas for charts, native KPIs/charts. Dashboard + data + compute in ONE
# place — zero data movement, no external server to host or secure.
# NEXT: Project 18 — real-time fraud detection.
# ============================================================================
