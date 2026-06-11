import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# PAGE CONFIG
st.set_page_config(
    page_title="Loan Portfolio Health Monitor",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/clean_loan_data.csv",
        usecols=[
            "loan_amnt",
            "grade",
            "purpose",
            "loan_status",
            "is_npa",
            "issue_year",
            "dti"
        ]
    )

@st.cache_data
def get_heatmap_data(df):
    return pd.pivot_table(
        df,
        values="is_npa",
        index="grade",
        columns="purpose",
        aggfunc="mean"
    ) * 100

@st.cache_data
def get_vintage_data(df):
    return (
        df.groupby("issue_year")["is_npa"]
        .mean() * 100
    )

# LOAD DATA
with st.spinner("Loading loan portfolio data..."):
    df = load_data()

st.title("Loan Portfolio Health Monitor Dashboard")
st.markdown("Interactive NPA Monitoring & Risk Analytics Dashboard")
# SIDEBAR
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio(
    "Select Page",
    [
        "Portfolio Overview",
        "NPA Deep Dive",
        "Vintage Tracker",
        "High Risk Accounts",
        "Repayment Health"
    ]
)
st.sidebar.header("Global Filters")
selected_grades = st.sidebar.multiselect(
    "Loan Grade",
    sorted(df["grade"].dropna().unique())
)

selected_purposes = st.sidebar.multiselect(
    "Purpose",
    sorted(df["purpose"].dropna().unique())
)

# ==========================================
# APPLY FILTERS
# ==========================================
filtered_df = df.copy()

if selected_grades:
    filtered_df = filtered_df[
        filtered_df["grade"].isin(selected_grades)
    ]

if selected_purposes:
    filtered_df = filtered_df[
        filtered_df["purpose"].isin(selected_purposes)
    ]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ==========================================
# PORTFOLIO OVERVIEW
# ==========================================
if page == "Portfolio Overview":

    st.header("Portfolio Overview")

    total_loans = len(filtered_df)
    total_loan_value = filtered_df["loan_amnt"].sum()
    npa_rate = filtered_df["is_npa"].mean() * 100

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Loans",
        f"{total_loans:,}"
    )

    col2.metric(
        "Total Loan Value",
        f"${total_loan_value:,.0f}"
    )

    col3.metric(
        "Overall NPA Rate",
        f"{npa_rate:.2f}%"
    )

    st.subheader("Loans by Grade")

    st.bar_chart(
        filtered_df["grade"].value_counts()
    )

    st.subheader("Loan Status Breakdown")

    st.bar_chart(
        filtered_df["loan_status"].value_counts()
    )
# NPA DEEP DIVE
elif page == "NPA Deep Dive":

    st.header("NPA Deep Dive")

    purpose = st.selectbox(
        "Select Purpose",
        sorted(filtered_df["purpose"].dropna().unique())
    )

    temp_df = filtered_df[
        filtered_df["purpose"] == purpose
    ]

    st.subheader("NPA Rate by Grade")

    grade_npa = (
        temp_df.groupby("grade")["is_npa"]
        .mean() * 100
    )

    st.bar_chart(grade_npa)

    st.subheader("Grade vs Purpose Risk Heatmap")

    heatmap_data = get_heatmap_data(filtered_df)

    fig, ax = plt.subplots(figsize=(12,6))

    sns.heatmap(
        heatmap_data,
        cmap="Reds",
        annot=True,
        fmt=".1f",
        ax=ax
    )

    st.pyplot(fig)

# ==========================================
# VINTAGE TRACKER
# ==========================================
elif page == "Vintage Tracker":

    st.header("Vintage Tracker")

    vintage = get_vintage_data(filtered_df)

    st.subheader("NPA Rate by Issue Year")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(
        vintage.index,
        vintage.values,
        marker="o"
    )

    ax.set_xlabel("Issue Year")
    ax.set_ylabel("NPA Rate (%)")
    ax.set_title("Vintage Analysis")
    ax.grid(True)

    st.pyplot(fig)

    st.subheader("Vintage Metrics")

    vintage_table = (
        filtered_df.groupby("issue_year")
        .agg({
            "loan_amnt": "mean",
            "dti": "mean",
            "is_npa": "mean"
        })
        .reset_index()
    )

    vintage_table.columns = [
        "Issue Year",
        "Avg Loan Amount",
        "Avg DTI",
        "NPA Rate"
    ]

    vintage_table["NPA Rate"] = (
        vintage_table["NPA Rate"] * 100
    )

    st.dataframe(vintage_table)

# ==========================================
# HIGH RISK ACCOUNTS
# ==========================================
elif page == "High Risk Accounts":

    st.header("High Risk Accounts")

    try:

        risk_df = pd.read_csv(
            "data/processed/flagged_accounts.csv"
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Total High Risk Accounts",
            f"{len(risk_df):,}"
        )

        if "loan_amnt" in risk_df.columns:
            col2.metric(
                "High Risk Exposure",
                f"${risk_df['loan_amnt'].sum():,.0f}"
            )

        st.subheader("Flagged Accounts")

        st.dataframe(
    risk_df.head(1000),
    use_container_width=True
)

        csv = risk_df.to_csv(index=False)

        st.download_button(
            label="📥 Download High Risk Loans CSV",
            data=csv,
            file_name="high_risk_loans.csv",
            mime="text/csv"
        )

    except Exception:
        st.error(
            "flagged_accounts.csv not found in data/processed/"
        )

# ==========================================
# REPAYMENT HEALTH
# ==========================================
elif page == "Repayment Health":

    st.header("Repayment Health")

    st.subheader("Loan Status Distribution")

    status_counts = (
        filtered_df["loan_status"]
        .value_counts()
    )

    st.bar_chart(status_counts)

    st.subheader("Recovery Rate by Grade")

    recovery = (
        filtered_df.groupby("grade")
        .apply(
            lambda x:
            (
                x["loan_status"]
                .eq("Fully Paid")
                .mean()
            ) * 100
        )
    )

    st.bar_chart(recovery)

    fully_paid = (
        filtered_df["loan_status"]
        .eq("Fully Paid")
        .mean()
        * 100
    )

    current = (
        filtered_df["loan_status"]
        .eq("Current")
        .mean()
        * 100
    )

    charged_off = (
        filtered_df["loan_status"]
        .eq("Charged Off")
        .mean()
        * 100
    )

    st.subheader("Repayment Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Fully Paid %",
        f"{fully_paid:.2f}%"
    )

    col2.metric(
        "Current %",
        f"{current:.2f}%"
    )

    col3.metric(
        "Charged Off %",
        f"{charged_off:.2f}%"
    )