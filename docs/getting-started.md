---
layout: page
title: Getting Started
permalink: /getting-started/
---

# Getting Started

This guide walks you through setting up IKYEASight locally and running the Streamlit dashboard.

---

## Prerequisites

- Python 3.10+
- Access to the IKYEA Odoo PostgreSQL databases (credentials required)
- Internet connection for geocoding via Nominatim

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/otalfredo8/ikyeasight.git
cd ikyeasight
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Configuration

Database connection strings are managed via [Streamlit Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

Create `.streamlit/secrets.toml` locally:

```toml
DB_CLOTHING   = "postgresql://user:password@host:5432/dbname"
DB_FURNITURE  = "postgresql://user:password@host:5432/dbname"
DB_RESTAURANT = "postgresql://user:password@host:5432/dbname"
```

> ⚠️ Never commit `secrets.toml` to version control. It is already in `.gitignore`.

---

## Running the Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Dashboard Controls

| Button | Action |
|---|---|
| 🔍 Test Database Connections | Verify connectivity to all three Odoo databases |
| ⚡ Use Cached Data | Load previously geocoded partner data from disk (fast) |
| 🔄 Sync & Geocode | Fetch live data from Odoo and geocode addresses (slow, first time) |

---

## Running the CLI Script

The `main.py` script runs the full MVC pipeline headlessly and saves outputs to disk.

```bash
python main.py
```

**Outputs:**
- `data/partners_processed_coordinates.parquet` — cached geocoded partner data
- `outputs/IKYEA_Partner_Map2.html` — standalone interactive HTML map

---

## Project Structure

```
ikyeasight/
├── main.py                  # CLI entry point (headless MVC pipeline)
├── streamlit_app.py         # Streamlit web dashboard
├── requirements.txt         # Python dependencies
├── Queries.sql              # Reference SQL queries for Odoo
├── data/                    # Data files (CSV, Parquet cache)
├── outputs/                 # Generated map HTML files
├── docs/                    # GitHub Pages documentation
└── src/
    ├── models/
    │   ├── database.py      # PartnerModel — fetches data from Odoo
    │   └── queries.py       # SQL query constants
    ├── controllers/
    │   └── geo_controller.py # GeoController — geocodes addresses
    └── views/
        └── map_view.py      # MapView — renders Folium map
```
