---
layout: page
title: Architecture
permalink: /architecture/
---

# Architecture

IKYEASight follows the **Model-View-Controller (MVC)** pattern. Each layer has a single, well-defined responsibility.

---

## MVC Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                    streamlit_app.py / main.py            │
│  (Entry Point — wires MVC components together)          │
└────────────┬──────────────┬───────────────┬─────────────┘
             │              │               │
      ┌──────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
      │   MODEL     │ │ CONTROLLER │ │    VIEW     │
      │ database.py │ │ geo_ctrl.py│ │ map_view.py │
      │ queries.py  │ │            │ │             │
      └──────┬──────┘ └─────┬──────┘ └─────┬──────┘
             │              │               │
      Fetch from       Geocode         Render Folium
      Odoo DBs         addresses       map with
      via SQL          via Nominatim   clustered markers
```

---

## Components

### Model — `src/models/`

**`database.py` — `PartnerModel`**

Connects to each brand's Odoo PostgreSQL database and returns a combined DataFrame.

- Iterates over the `config` dict (`brand → connection_string`)
- Uses SQLAlchemy to execute `GET_PARTNERS` query against each database
- Appends a `brand` column to identify the source
- Returns a single concatenated `pd.DataFrame`

**`queries.py` — SQL constants**

Stores the `GET_PARTNERS` SQL query that joins `res_partner` with `res_country` to get name, address fields, coordinates, and country code for active, non-company partners.

---

### Controller — `src/controllers/`

**`geo_controller.py` — `GeoController`**

Cleans and geocodes partner addresses using the [Geopy](https://geopy.readthedocs.io/) Nominatim client.

- `clean_address(row)` — formats a row into a geocoding-friendly string: `"street, city, zip, country_code"`
- `process_coordinates(df)` — iterates over rows with missing/zero coordinates and calls Nominatim; falls back to `city, zip` if the full address fails
- Uses `RateLimiter` (1 second between requests) to comply with Nominatim's usage policy

---

### View — `src/views/`

**`map_view.py` — `MapView`**

Renders an interactive Folium map with clustered markers color-coded by brand.

- Initializes a `folium.Map` centered on the continental US
- Uses `MarkerCluster` to group nearby markers and avoid clutter
- Assigns brand colors: I-Clothing → blue, I-Furniture → green, I-Restaurant → orange
- Popups display the partner name on click

---

## Entry Points

### `main.py` (CLI / Headless)

Runs the full pipeline without a browser:
1. `PartnerModel.fetch_all_data()` — fetch from all three databases
2. `GeoController.process_coordinates()` — geocode
3. Cache result to `data/partners_processed_coordinates.parquet`
4. `MapView.render()` — build map
5. Save map to `outputs/IKYEA_Partner_Map2.html`

### `streamlit_app.py` (Web Dashboard)

Provides an interactive UI:
- Sidebar buttons to test DB connections, load cached data, or trigger a full sync
- Map rendered inline using `streamlit-folium`
- Raw data table with CSV download

---

## Caching Strategy

To avoid re-geocoding on every run (Nominatim is rate-limited), processed coordinates are cached as a Parquet file at `data/partners_processed_coordinates.parquet`. The "Use Cached Data" button in the dashboard loads this file directly, skipping the geocoding step entirely.

---

## Technology Stack

| Layer | Library |
|---|---|
| Web dashboard | [Streamlit](https://streamlit.io/) |
| Map rendering | [Folium](https://python-visualization.github.io/folium/) + [streamlit-folium](https://folium.streamlit.app/) |
| Geocoding | [Geopy](https://geopy.readthedocs.io/) (Nominatim / OpenStreetMap) |
| Database | [SQLAlchemy](https://www.sqlalchemy.org/) + [psycopg2](https://www.psycopg.org/) |
| Data processing | [Pandas](https://pandas.pydata.org/) + [PyArrow](https://arrow.apache.org/docs/python/) |
