# TikTok Shop Merchant Onboarding Analytics & Experimentation Platform (TS-MAE)

## Project Overview
This enterprise analytics project addresses merchant funnel drop-off and post-onboarding 30-day GMV stagnation across TikTok Shop US operations. Built using Google BigQuery SQL, Python statistical modules, and Looker Studio, this platform processes 50,000 merchant onboarding logs to evaluate product bottlenecks and measure the lift of a new portal onboarding experience (Variant v2.0).

## Repository Architecture
- `scripts/data_generation.py`: Python script for synthetic dataset generation (50,000 records).
- `sql/bigquery_transformations.sql`: Advanced SQL transformations, ETL pipeline logic, and analytical view creation.
- `notebooks/ab_testing_analysis.ipynb`: Statistical hypothesis testing script executing pooled Z-tests for activation lift.
- `data/tiktok_shop_google_sheets_model.csv`: Generated summary ledger representing Google Sheets export of key metrics.
- `Executive_Summary.md`: C-suite business briefing and strategic implementation roadmap.
- `Dashboard_Executive_Summary.md`: User manual and metric guide for the Looker Studio executive dashboard.
- `Project_Disclaimer.md`: Data governance, compliance, and synthetic generation notice.

## Tech Stack
- Data Warehousing: Google BigQuery (`driiiportfolio.tiktok_shop_analytics`)
- Data Processing & Experimentation: Python (Pandas, SciPy, NumPy)
- Business Intelligence: Google Looker Studio
- Version Control: GitHub
