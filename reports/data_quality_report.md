# Data Quality Report

## Original Dataset
- Rows: 2,260,701
- Columns: 151

## Final Dataset
- Rows: 2,257,952
- Columns: 110

## Cleaning Steps
1. Removed columns with >40% missing values.
2. Dropped id and member_id.
3. Converted date columns.
4. Cleaned int_rate.
5. Cleaned revol_util.
6. Cleaned emp_length.
7. Removed invalid loan statuses.
8. Created is_npa feature.
9. Created loan_to_income feature.
10. Created issue_year, issue_month, loan_age_months, grade_numeric.

## Top Missing Columns
- member_id (100%)
- hardship_reason (99.5%)
- hardship_status (99.5%)
- ...