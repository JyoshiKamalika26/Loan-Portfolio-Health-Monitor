from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder
from config import *
import pandas as pd
import numpy as np
import logging
# LOGGING
logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# FASTAPI APP
app = FastAPI(
    title="Loan Portfolio Health Monitor API"
)
# DATABASE CONNECTION
try:

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    connection = engine.connect()
    connection.close()

    logging.info("Database connection successful")

except SQLAlchemyError as e:

    logging.error(f"Database Connection Error : {str(e)}")

    raise Exception("Unable to connect to database")
# DATA CLEANING FUNCTION
def clean_df(df):

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna("")

    for col in df.columns:

        if "date" in col.lower() or "_d" in col.lower():

            df[col] = df[col].astype(str)

    return jsonable_encoder(
        df.to_dict(orient="records")
    )
# COMMON QUERY FUNCTION
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

        logging.error(f"SQLAlchemy Error : {str(e)}")

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

    except TypeError as e:

        logging.error(f"Type Error : {str(e)}")

        raise HTTPException(
            status_code=400,
            detail="Datatype Error"
        )

    except KeyError as e:

        logging.error(f"Key Error : {str(e)}")

        raise HTTPException(
            status_code=400,
            detail="Column Missing"
        )

    except ConnectionError as e:

        logging.error(f"Connection Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Connection Failed"
        )

    except HTTPException:
        raise

    except Exception as e:

        logging.error(f"Unexpected Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
# HOME
@app.get("/")
def home():

    try:

        logging.info("Home API Called")

        return {
            "message": "Loan Portfolio Health Monitor API Running"
        }

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Server Error"
        )
# SUMMARY
@app.get("/summary")
def summary():

    try:

        logging.info("/summary API Called")

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

    except HTTPException:
        raise

    except Exception as e:

        logging.error(f"/summary Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch summary"
        )
# SAMPLE LOANS
@app.get("/loans")
def loans(limit: int = 100):

    try:

        if limit <= 0:

            raise HTTPException(
                status_code=400,
                detail="Limit must be greater than zero"
            )

        query = f"""
        SELECT *
        FROM clean_loan_data
        LIMIT {limit}
        """

        return execute_query(query)

    except HTTPException:
        raise

    except Exception as e:

        logging.error(f"/loans Error : {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch loans"
        )
# LOAN STATUS
@app.get("/loan_status")
def loan_status():

    try:

        query = """
        SELECT
            loan_status,
            COUNT(*) total
        FROM clean_loan_data
        GROUP BY loan_status
        ORDER BY total DESC
        """

        return execute_query(query)

    except HTTPException:
        raise

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch loan status"
        )
# GRADE DISTRIBUTION
@app.get("/grade_distribution")
def grade_distribution():

    try:

        query = """
        SELECT
            grade,
            COUNT(*) total
        FROM clean_loan_data
        GROUP BY grade
        ORDER BY grade
        """

        return execute_query(query)

    except HTTPException:
        raise

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch grade distribution"
        )
# PURPOSE DISTRIBUTION
@app.get("/purpose_distribution")
def purpose_distribution():

    try:

        query = """
        SELECT
            purpose,
            COUNT(*) total
        FROM clean_loan_data
        GROUP BY purpose
        ORDER BY total DESC
        """

        return execute_query(query)

    except HTTPException:
        raise

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch purpose distribution"
        )
# HOME OWNERSHIP
@app.get("/home_ownership")
def home_ownership():

    try:

        query = """
        SELECT
            home_ownership,
            COUNT(*) total
        FROM clean_loan_data
        GROUP BY home_ownership
        """

        return execute_query(query)

    except HTTPException:
        raise

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch home ownership"
        )
# NPA BY GRADE
@app.get("/npa_by_grade")
def npa_by_grade():

    try:

        query = """
        SELECT
            grade,
            ROUND(AVG(is_npa)*100,2) npa_rate
        FROM clean_loan_data
        GROUP BY grade
        ORDER BY grade
        """

        return execute_query(query)

    except HTTPException:
        raise

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch NPA by grade"
        )
# NPA BY YEAR
@app.get("/npa_by_year")
def npa_by_year():

    try:

        query = """
        SELECT
            issue_year,
            ROUND(AVG(is_npa)*100,2) npa_rate
        FROM clean_loan_data
        GROUP BY issue_year
        ORDER BY issue_year
        """

        return execute_query(query)

    except HTTPException:
        raise

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch NPA by year"
        )
# HIGH RISK LOANS
@app.get("/high_risk")
def high_risk():

    try:

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

    except HTTPException:
        raise

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch high risk loans"
        )