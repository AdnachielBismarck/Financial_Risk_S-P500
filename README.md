# Financial Risk Monitoring Dashboard

## Overview

This project presents a **data-driven framework for monitoring financial market risk** using statistical modeling and interactive visualization.

The system identifies **extreme market events** and models their dynamics through:

- Volatility estimation (GARCH)
- Event intensity modeling (Poisson process)

The result is an **interactive dashboard** that allows users to explore how risk evolves over time.

---

## Problem Statement

Financial markets are characterized by:

- Sudden extreme events (crashes, shocks)
- Time-varying volatility
- Clustering of risk

Traditional static metrics fail to capture these dynamics.

This project addresses this gap by building a **dynamic risk monitoring system**.

---

## Methodology

### 1. Data Collection
- Historical S&P 500 price data
- Daily frequency

### 2. Feature Engineering
- Log returns
- Volatility proxy
- Extreme event detection (percentile threshold)

### 3. Modeling

#### Volatility Model
- GARCH(1,1)
- Captures volatility clustering

#### Event Model
- Poisson-based intensity λ(t)
- Measures frequency of extreme events

---

## Dashboard Features

- Market price evolution
- Return series with extreme events
- Time-varying volatility
- Dynamic risk intensity λ(t)

Interactive filters:
- Date range selection

---

## Key Insights

- Risk is **not constant** — it evolves dynamically  
- Extreme events tend to **cluster in time**  
- High volatility regimes correspond to **increased event intensity**  

---

## Demo

The dashboard is deployed and allows interactive exploration of market risk.

*(Add your Render link here)*

---

## Tech Stack

- Python
- Pandas
- ARCH (GARCH modeling)
- Dash (interactive dashboard)
- Plotly

---

## Project Structure

Financial_Risk_Project/
│
├── data/
│ ├── raw/
│ └── processed/
│
├── notebooks/
│ ├── 01_data_collection.ipynb
│ ├── 02_feature_engineering.ipynb
│ ├── 03_modeling.ipynb
│
├── src/
│ ├── features.py
│ ├── models.py
│ └── utils.py
│
├── app/
│ └── app.py
│
├── reports/
│ └── executive_report.pdf
│
├── requirements.txt
├── render.yaml
└── README.md


---

## Limitations

- Based on historical data
- Does not include macroeconomic variables
- Simplified event modeling assumptions

---

## Future Work

- Regime detection (under development)
- Real-time data integration
- Predictive risk modeling

---

## Author

Adnachiel Bismarck Avendaño Chavez

---
