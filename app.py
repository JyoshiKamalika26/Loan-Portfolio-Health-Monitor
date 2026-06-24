import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL Connection
engine = create_engine(
    "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/loan_portfolio_db"
)

# Load Data from PostgreSQL
@st.cache_data
def load_data():

    query = """
    SELECT
        loan_amnt,
        grade,
        purpose,
        loan_status,
        is_npa,
        issue_year,
        dti
    FROM loans
    """

    return pd.read_sql(query, engine)

# Read Data
df = load_data()

# Dashboard Title
st.set_page_config(
    page_title="Loan Portfolio Health Monitor",
    layout="wide"
)

st.title("📊 Loan Portfolio Health Monitor")

# Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Total Loans
st.metric(
    "Total Loans",
    len(df)
)

# NPA Rate
npa_rate = round(df["is_npa"].mean() * 100, 2)

st.metric(
    "NPA Rate (%)",
    npa_rate
)

# Grade Wise NPA
st.subheader("Grade Wise NPA")

grade_npa = (
    df.groupby("grade")["is_npa"]
    .mean()
    .reset_index()
)

st.bar_chart(
    grade_npa.set_index("grade")
)

# Purpose Wise Loans
st.subheader("Loan Purpose Distribution")

purpose_count = (
    df["purpose"]
    .value_counts()
)

st.bar_chart(purpose_count)

# Vintage Analysis
st.subheader("Vintage Analysis")

vintage = (
    df.groupby("issue_year")["is_npa"]
    .mean()
    .reset_index()
)

st.line_chart(
    vintage.set_index("issue_year")
)