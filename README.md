# Loan Portfolio Health Monitor

An interactive Streamlit dashboard for monitoring loan portfolio performance, Non-Performing Assets (NPA), repayment health, and high-risk accounts.

---

## Project Overview

This project analyzes a large-scale loan dataset and provides actionable insights into portfolio risk, repayment behavior, and loan performance. The dashboard enables decision-makers to monitor portfolio health through interactive visualizations and risk analytics.

---

## Features

### Portfolio Overview
- Total Loans
- Total Loan Value
- Overall NPA Rate
- Loan Status Distribution

### NPA Deep Dive
- Grade-wise NPA Analysis
- Purpose-wise Risk Analysis
- Interactive Risk Heatmap

### Vintage Tracker
- NPA Trend by Issue Year
- Vintage Performance Metrics

### High Risk Accounts
- Early Warning System
- Flagged High-Risk Loans
- CSV Download Option

### Repayment Health
- Loan Status Monitoring
- Recovery Rate Analysis
- Repayment Summary Metrics

---

## Project Structure

```text
Loan_Portfolio_Health_Monitor/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   └── processed/
│       ├── clean_loan_data.csv
│       └── flagged_accounts.csv
│
├── notebooks/
│   ├── task1_data_cleaning.py
│   ├── task2_risk_analytics.py
│   └── week3_npa_analysis.ipynb
│
├── outputs/
│   ├── risk_heatmap.png
│   ├── vintage_analysis.png
│   ├── metrics_summary.csv
│   └── charts/
│       └── eda_dashboard.png
│
└── .gitignore
```

---

## Installation & Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Loan_Portfolio_Health_Monitor
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Verify Data Files

Ensure the following files exist:

```text
data/processed/clean_loan_data.csv
data/processed/flagged_accounts.csv
```

---

## Running the Project

### Task 1 – Data Cleaning

```bash
python notebooks/task1_data_cleaning.py
```

Output:

```text
data/processed/clean_loan_data.csv
```

---

### Task 2 – Risk Analytics

```bash
python notebooks/task2_risk_analytics.py
```

Outputs:

```text
data/processed/flagged_accounts.csv
outputs/risk_heatmap.png
outputs/vintage_analysis.png
outputs/metrics_summary.csv
```

---

### Task 3 – Streamlit Dashboard

```bash
streamlit run app.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

## Key Results

### Portfolio Statistics

| Metric           | Value         |
|------------------|---------------|
| Total Loans      | 2,257,952     |
| Overall NPA Rate | 11.90%        |
| High Risk Loans  | 29,538        |

### Risk Distribution

| Risk Category | Count     |
|-------------------------- |
| Low Risk      | 1,745,589 |
| Medium Risk   | 482,825   |
| High Risk     | 29,538    |

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Git
- GitHub

---

## Dashboard Navigation

Use the sidebar to access:

1. Portfolio Overview
2. NPA Deep Dive
3. Vintage Tracker
4. High Risk Accounts
5. Repayment Health

Global Filters:

- Loan Grade
- Loan Purpose


## Conclusion

The Loan Portfolio Health Monitor provides a comprehensive solution for analyzing loan performance, identifying risky accounts, tracking NPA trends, and monitoring repayment health. The project demonstrates practical applications of data analytics, risk assessment, and dashboard development in the financial services domain.