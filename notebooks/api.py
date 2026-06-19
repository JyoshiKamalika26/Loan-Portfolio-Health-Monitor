from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus
from fastapi.encoders import jsonable_encoder
import pandas as pd
import numpy as np
import logging

# ==================================================
# LOGGING
# ==================================================
logging.basicConfig(
    filename="api_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==================================================
# FASTAPI APP
# ==================================================
app = FastAPI(
    title="Loan Portfolio Health Monitor API"
)

# ==================================================
# DATABASE CONNECTION
# ==================================================
try:

    password = quote_plus("Srithu@1808")

    engine = create_engine(
        f"postgresql+psycopg2://postgres:{password}@localhost:3307/loan_portfolio"
    )

except SQLAlchemyError as e:

    logging.error(str(e))

    raise Exception("Database connection failed")


# ==================================================
# DATA CLEANING FUNCTION
# ==================================================
def clean_df(df):

    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.fillna("")

    for col in df.columns:

        if "date" in col.lower() or "_d" in col.lower():

            df[col] = df[col].astype(str)

    return jsonable_encoder(
        df.to_dict(orient="records")
    )


# ==================================================
# COMMON QUERY FUNCTION
# ==================================================
def execute_query(query):

    try:

        df = pd.read_sql(query, engine)

        if df.empty:

            raise HTTPException(
                status_code=404,
                detail="No records found"
            )

        return clean_df(df)

    except SQLAlchemyError as e:

        logging.error(f"Database Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Database Error"
        )

    except ValueError as e:

        logging.error(f"Value Error : {str(e)}")

        raise HTTPException(
            status_code=400,
            detail="Invalid Data"
        )

    except KeyError as e:

        logging.error(f"Key Error : {str(e)}")

        raise HTTPException(
            status_code=400,
            detail="Column Missing"
        )

    except Exception as e:

        logging.error(f"Unexpected Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


# ==================================================
# HOME
# ==================================================
@app.get("/")
def home():

    return {
        "message":
        "Loan Portfolio Health Monitor API Running"
    }


# ==================================================
# SUMMARY
# ==================================================
@app.get("/summary")
def summary():

    query = """
    SELECT
        COUNT(*) total_loans,
        ROUND(AVG(loan_amnt)::numeric,2) avg_loan_amount,
        ROUND(AVG(annual_inc)::numeric,2) avg_annual_income,
        ROUND(AVG(int_rate)::numeric,2) avg_interest_rate,
        ROUND(SUM(loan_amnt)::numeric,2) total_disbursed_amount
    FROM clean_loan_data
    """

    return execute_query(query)


# ==================================================
# SAMPLE LOANS
# ==================================================
@app.get("/loans")
def loans(limit: int = 100):

    if limit <= 0:

        raise HTTPException(
            status_code=400,
            detail="Limit must be greater than 0"
        )

    query = f"""
    SELECT *
    FROM clean_loan_data
    LIMIT {limit}
    """

    return execute_query(query)


# ==================================================
# LOAN STATUS
# ==================================================
@app.get("/loan_status")
def loan_status():

    query = """
    SELECT
        loan_status,
        COUNT(*) total
    FROM clean_loan_data
    GROUP BY loan_status
    ORDER BY total DESC
    """

    return execute_query(query)


# ==================================================
# GRADE DISTRIBUTION
# ==================================================
@app.get("/grade_distribution")
def grade_distribution():

    query = """
    SELECT
        grade,
        COUNT(*) total
    FROM clean_loan_data
    GROUP BY grade
    ORDER BY grade
    """

    return execute_query(query)


# ==================================================
# PURPOSE DISTRIBUTION
# ==================================================
@app.get("/purpose_distribution")
def purpose_distribution():

    query = """
    SELECT
        purpose,
        COUNT(*) total
    FROM clean_loan_data
    GROUP BY purpose
    ORDER BY total DESC
    """

    return execute_query(query)


# ==================================================
# HOME OWNERSHIP
# ==================================================
@app.get("/home_ownership")
def home_ownership():

    query = """
    SELECT
        home_ownership,
        COUNT(*) total
    FROM clean_loan_data
    GROUP BY home_ownership
    """

    return execute_query(query)


# ==================================================
# NPA BY GRADE
# ==================================================
@app.get("/npa_by_grade")
def npa_by_grade():

    query = """
    SELECT
        grade,
        ROUND(AVG(is_npa)*100,2) npa_rate
    FROM clean_loan_data
    GROUP BY grade
    ORDER BY grade
    """

    return execute_query(query)


# ==================================================
# NPA BY YEAR
# ==================================================
@app.get("/npa_by_year")
def npa_by_year():

    query = """
    SELECT
        issue_year,
        ROUND(AVG(is_npa)*100,2) npa_rate
    FROM clean_loan_data
    GROUP BY issue_year
    ORDER BY issue_year
    """

    return execute_query(query)


# ==================================================
# HIGH RISK LOANS
# ==================================================
@app.get("/high_risk")
def high_risk():

    query = """
    SELECT
        loan_amnt,
        grade,
        dti,
        annual_inc,
        loan_status
    FROM clean_loan_data
    WHERE grade_numeric >= 6
    AND dti > 20
    LIMIT 100
    """

    return execute_query(query)