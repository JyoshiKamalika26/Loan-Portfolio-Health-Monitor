import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from config import *
import plotly.express as px

# ===================================
# PAGE CONFIG
# ===================================
st.set_page_config(
    page_title="Loan Portfolio Health Monitor",
    layout="wide"
)

st.title("🏦 Loan Portfolio Health Monitor")

# ===================================
# DATABASE CONNECTION
# ===================================
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
# ===================================
# GLOBAL FILTERS
# ===================================
st.sidebar.header("Global Filters")

# Grade List
grade_query = """
SELECT DISTINCT grade
FROM clean_loan_data
ORDER BY grade
"""

grade_list = pd.read_sql(grade_query, engine)["grade"].tolist()

selected_grade = st.sidebar.selectbox(
    "Select Grade",
    ["All"] + grade_list
)

# Purpose List
purpose_query = """
SELECT DISTINCT purpose
FROM clean_loan_data
ORDER BY purpose
"""

purpose_list = pd.read_sql(purpose_query, engine)["purpose"].tolist()

selected_purpose = st.sidebar.selectbox(
    "Select Purpose",
    ["All"] + purpose_list
)
# ===================================
# FILTER CONDITION
# ===================================
condition = "WHERE 1=1"

if selected_grade != "All":
    condition += f" AND grade='{selected_grade}'"

if selected_purpose != "All":
    condition += f" AND purpose='{selected_purpose}'"
   
# ===================================
# PORTFOLIO OVERVIEW
# ===================================
st.header("📊 Portfolio Overview")

query = f"""
SELECT
COUNT(*) total_loans,
ROUND(SUM(loan_amnt)::numeric,2) total_loan_value,
ROUND(AVG(is_npa)*100,2) overall_npa_rate,
ROUND(AVG(recoveries)::numeric,2) avg_recovery
FROM clean_loan_data
{condition}
"""

overview_df = pd.read_sql(query, engine)

total_loans = overview_df["total_loans"][0]
total_loan_value = overview_df["total_loan_value"][0]
overall_npa_rate = overview_df["overall_npa_rate"][0]
avg_recovery = overview_df["avg_recovery"][0]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Loans", f"{total_loans:,}")

col2.metric(
    "Total Loan Value",
    f"${total_loan_value:,.0f}"
)

col3.metric(
    "Overall NPA Rate",
    f"{overall_npa_rate}%"
)

col4.metric(
    "Avg Recovery",
    f"${avg_recovery:,.0f}"
)
st.subheader("Loan Count by Grade")

query = f"""
SELECT
grade,
COUNT(*) total_loans
FROM clean_loan_data
{condition}
GROUP BY grade
ORDER BY grade
"""

grade_df = pd.read_sql(query, engine)

st.bar_chart(
    grade_df.set_index("grade")
)
st.subheader("Loan Status Distribution")

query = f"""
SELECT
loan_status,
COUNT(*) total
FROM clean_loan_data
{condition}
GROUP BY loan_status
"""

status_df = pd.read_sql(query, engine)

fig = px.pie(
    status_df,
    names="loan_status",
    values="total",
    title="Loan Status Distribution"
)

st.plotly_chart(fig, use_container_width=True)
# ===================================
# NPA DEEP DIVE
# ===================================
st.header("📉 NPA Deep Dive")
# Loan Amount Slider
loan_range = st.slider(
    "Select Loan Amount Range",
    0,
    40000,
    (0, 40000)
)

min_amt, max_amt = loan_range
condition2 = condition + f"""
 AND loan_amnt BETWEEN {min_amt} AND {max_amt}
"""
st.subheader("NPA Rate by Grade")

query = f"""
SELECT
grade,
ROUND(AVG(is_npa)*100,2) npa_rate
FROM clean_loan_data
{condition2}
GROUP BY grade
ORDER BY grade
"""

npa_grade_df = pd.read_sql(query, engine)

st.bar_chart(
    npa_grade_df.set_index("grade")
)
st.subheader("Grade vs Purpose Heatmap")

query = f"""
SELECT
grade,
purpose,
COUNT(*) total_loans
FROM clean_loan_data
{condition2}
GROUP BY grade,purpose
"""

heatmap_df = pd.read_sql(query, engine)

heatmap = heatmap_df.pivot(
    index="grade",
    columns="purpose",
    values="total_loans"
)

fig = px.imshow(
    heatmap,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig, use_container_width=True)
# ===================================
# HIGH RISK ACCOUNTS
# ===================================
st.header("⚠ High Risk Accounts")

query = f"""
SELECT
loan_amnt,
grade,
purpose,
dti,
annual_inc,
loan_status
FROM clean_loan_data
{condition}
AND grade_numeric >= 6
AND dti > 20
LIMIT 100
"""

risk_df = pd.read_sql(query, engine)

st.dataframe(risk_df)
csv = risk_df.to_csv(index=False)

st.download_button(
    "Download High Risk Accounts",
    csv,
    file_name="high_risk_accounts.csv",
    mime="text/csv"
)
# ===================================
# VINTAGE TRACKER
# ===================================
st.header("📈 Vintage Tracker")

query = f"""
SELECT
issue_year,
ROUND(AVG(is_npa)*100,2) AS npa_rate
FROM clean_loan_data
{condition}
GROUP BY issue_year
ORDER BY issue_year
"""

vintage_df = pd.read_sql(query, engine)

fig = px.line(
    vintage_df,
    x="issue_year",
    y="npa_rate",
    markers=True,
    title="NPA Trend by Issue Year"
)

st.plotly_chart(fig, use_container_width=True)
# ===================================
# REPAYMENT HEALTH
# ===================================
st.header("💰 Repayment Health")

query = f"""
SELECT
grade,
ROUND(AVG(recoveries)::numeric,2) recovery_rate
FROM clean_loan_data
{condition}
GROUP BY grade
ORDER BY grade
"""

recovery_df = pd.read_sql(query, engine)

fig = px.bar(
    recovery_df,
    x="grade",
    y="recovery_rate",
    color="grade",
    title="Recovery Rate by Grade"
)

st.plotly_chart(fig, use_container_width=True)
# ===================================
# TOP 100 LOANS
# ===================================
st.header("📋 Loan Details")

query = f"""
SELECT
loan_amnt,
funded_amnt,
grade,
purpose,
annual_inc,
dti,
loan_status
FROM clean_loan_data
{condition}
LIMIT 100
"""

loan_df = pd.read_sql(query, engine)

st.dataframe(
    loan_df,
    use_container_width=True
)
# ===================================
# DOWNLOAD DATA
# ===================================
csv = loan_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Loan Data",
    data=csv,
    file_name="loan_data.csv",
    mime="text/csv"
)