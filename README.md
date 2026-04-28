# Financial Risk Monitoring Dashboard

## Live Application

https://financial-risk-dashboard.onrender.com/

---

## Executive Summary

This project develops a **data-driven financial risk monitoring system** for the S&P 500, integrating econometric models and interactive visualization to analyze how market risk evolves over time.

The system combines:

- Volatility modeling (GARCH)
- Extreme event detection
- Event intensity estimation (Poisson process)

to provide a **dynamic view of financial risk**, enabling deeper analysis beyond traditional static metrics.

---

## Business Problem

Financial markets are inherently unstable and exhibit:

- Volatility clustering  
- Sudden extreme events (crashes, shocks)  
- Non-constant risk regimes  

Most traditional approaches rely on **static risk measures**, which fail to capture these dynamics.

This project addresses this limitation by building a **dynamic risk monitoring framework**, allowing users to track how risk evolves and clusters over time.

---

## Analytical Approach

### Data Source
- Historical S&P 500 price data  
- Daily frequency  

---

### Feature Engineering

- Log returns  
- Rolling volatility proxy  
- Extreme event detection using percentile thresholds  

---

### Modeling

**1. Volatility Modeling**
- GARCH(1,1)
- Captures persistence and clustering in volatility

**2. Event Modeling**
- Poisson-based intensity function λ(t)
- Estimates frequency of extreme market events

---

## Dashboard Overview

The interactive dashboard enables users to:

- Analyze S&P 500 price evolution  
- Identify extreme return events  
- Track time-varying volatility  
- Monitor dynamic risk intensity λ(t)  

### Key Features

- Interactive date filtering  
- Multi-layer visualization (price, returns, volatility, events)  
- Real-time exploratory analysis of market regimes  

---

## Example Use Case

During periods of financial stress (e.g., crisis-like behavior), the model shows:

- Increased volatility (GARCH output)  
- Higher frequency of extreme returns  
- Elevated event intensity λ(t)  

This allows analysts to:

- Detect risk regime shifts  
- Identify clustering of extreme events  
- Support risk-aware decision-making  

---

## Key Insights

- Market risk is **time-varying and non-stationary**  
- Extreme events exhibit **temporal clustering**  
- Volatility and event intensity are **strongly correlated**  

These findings highlight the importance of **dynamic modeling in financial risk analysis**.

---

## Tech Stack

- Python  
- Pandas  
- ARCH (GARCH modeling)  
- Dash  
- Plotly  

---

## Project Structure

```bash
Financial_Risk_Project/
│
├── app/
│   ├── __init__.py
│   └── app.py                 # Dash application (entry point)
│
├── data/
│   ├── raw/                  # Original datasets
│   └── processed/            # Cleaned and feature-engineered data
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling.ipynb
│
├── reports/
│   └── Financial_Risk_Report.pdf   # Executive summary of findings
│
├── requirements.txt
├── render.yaml              # Deployment configuration (Render)
└── README.md
```
---

## Limitations

- Based exclusively on historical data  
- No integration of macroeconomic indicators  
- Simplified assumptions in Poisson event modeling  

---

## Future Improvements

- Regime-switching models (Markov Switching / HMM)  
- Real-time data ingestion (API integration)  
- Predictive risk modeling (forecasting volatility and events)  
- Portfolio-level risk extension  

---
## Run Locally

Clone the repository:

```bash
git clone https://github.com/AdnachielBismarck/Financial_Risk_S-P500.git
cd Financial_Risk_S-P500
```

Install dependencies:

- pip install -r requirements.txt

Run the application:

- python app/app.py

The app will be available at:

- http://127.0.0.1:8050/

## Author

Adnachiel Bismarck Avendaño Chavez