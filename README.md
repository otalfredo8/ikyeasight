# IKYEASight

![IKYEASight Dashboard](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![License](https://img.shields.io/badge/License-MIT-green)

**IKYEASight** is a Business Intelligence (BI) and Data Analytics initiative focused on the end-to-end lifecycle of IKYEA businesses' data. It provides real-time partner location mapping, income analysis, and geospatial insights through a modern, interactive dashboard.

🌍 **Live Dashboard**: [https://ikyeasight.streamlit.app/](https://ikyeasight.streamlit.app/)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Development Guide](#development-guide)
- [Data Sources](#data-sources)
- [Troubleshooting](#troubleshooting)
- [Infrastructure Setup](#infrastructure-setup)

---

## Overview

IKYEASight enables IKYEA business teams to:

- 📍 **Visualize Partner Locations**: Interactive global maps of partner networks across multiple brands
- 💰 **Analyze Income Data**: Correlation between business locations and regional income demographics
- 🔄 **Sync Multi-Database Systems**: Unified data collection from independent Odoo instances
- ⚡ **Real-Time Updates**: Live database connections with caching for performance optimization

### Key Statistics

- **Data Sources**: 3+ Odoo databases (I-Clothing, I-Furniture, I-Restaurant)
- **Geographic Coverage**: US-wide partner mapping with census data integration
- **Technology Stack**: Python 3.9+, Streamlit, SQLAlchemy, Folium, GeoPy

---

## Features

✅ **Multi-Database Integration**

- Connects to multiple Odoo instances simultaneously
- Aggregates partner data from I-Clothing, I-Furniture, and I-Restaurant brands
- Error handling with detailed connection diagnostics

✅ **Geospatial Intelligence**

- Automatic address geocoding using Nominatim (OpenStreetMap)
- Rate-limited requests to prevent API throttling
- Fallback geocoding strategies for incomplete addresses

✅ **Interactive Mapping**

- Clustered marker visualization with Folium
- Brand-specific color coding for easy identification
- Pan, zoom, and explore partner locations

✅ **Data Caching**

- Parquet format for efficient storage and retrieval
- Eliminates redundant geocoding requests
- Performance optimization for dashboard responsiveness

✅ **Census Data Integration**

- U.S. Census Bureau demographic data (2024 ACS 5-Year Estimates)
- Income analysis by region and partner location
- Economic insights for business strategy

---

## System Architecture

### Data Flow Architecture

```mermaid
flowchart LR
    DB1["🗄️ Odoo Database<br/>I-Clothing"]
    DB2["🗄️ Odoo Database<br/>I-Furniture"]
    DB3["🗄️ Odoo Database<br/>I-Restaurant"]
    CSV["📊 Census Data<br/>ACS 5-Year"]

    model["📦 PartnerModel<br/>fetch_all_data()"]
    controller["⚙️ GeoController<br/>process_coordinates()"]
    cache["💾 Cache Layer<br/>partners_processed.parquet"]
    view["🎨 MapView<br/>render()"]

    APP["🌐 Streamlit App<br/>Dashboard"]
    STATIC["📄 Static HTML<br/>maps"]

    DB1 -->|SQLAlchemy| model
    DB2 -->|SQLAlchemy| model
    DB3 -->|SQLAlchemy| model
    CSV -->|Pandas| view

    model -->|DataFrame| controller
    controller -->|Nominatim API| controller
    controller -->|Geocoded Data| cache
    cache -->|Read| view
    view -->|Folium Map| APP
    view -->|Export| STATIC

    style model fill:#e1f5ff
    style controller fill:#f3e5f5
    style view fill:#e8f5e9
    style cache fill:#fff3e0
```

### MVC Architecture Pattern

```mermaid
graph TB
    subgraph "Models"
        M1["PartnerModel<br/>Fetches from multiple Odoo DBs<br/>Handles connection logic"]
        M2["Queries.py<br/>SQL query constants"]
    end

    subgraph "Controllers"
        C1["GeoController<br/>Geocodes addresses<br/>Cleans data<br/>Manages geopy service"]
    end

    subgraph "Views"
        V1["MapView<br/>Renders interactive maps<br/>Handles styling & markers<br/>Exports to multiple formats"]
    end

    subgraph "Data Layer"
        D1["Parquet Cache"]
        D2["Database Connections"]
    end

    DB["Odoo Instances"]
    API["Nominatim API<br/>OpenStreetMap"]
    WEB["Streamlit App"]

    M1 --> M2
    M1 <--> D2
    D2 <--> DB
    M1 --> C1
    C1 <--> API
    C1 --> V1
    V1 <--> D1
    V1 --> WEB

    style M1 fill:#e1f5ff
    style C1 fill:#f3e5f5
    style V1 fill:#e8f5e9
```

### Component Responsibilities

| Component      | File                                | Responsibility                                                 |
| -------------- | ----------------------------------- | -------------------------------------------------------------- |
| **Model**      | `src/models/database.py`            | Fetch partner data from multiple Odoo databases via SQLAlchemy |
| **Queries**    | `src/models/queries.py`             | Store parameterized SQL queries as constants                   |
| **Controller** | `src/controllers/geo_controller.py` | Geocode addresses, clean data, handle geospatial processing    |
| **View**       | `src/views/map_view.py`             | Render Folium maps, style markers, export visualizations       |

---

## Installation & Setup

### Prerequisites

- **Python 3.9+**
- **pip** or **conda** package manager
- **Database Access**: Connection strings to Odoo instances (PostgreSQL)
- **Internet Connection**: For Nominatim geocoding API and Streamlit hosting

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/otalfredo8/ikyeasight.git
cd ikyeasight
```

#### 2. Create Virtual Environment

```bash
# Using venv (recommended)
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # macOS/Linux

# Or using conda
conda create -n ikyeasight python=3.9
conda activate ikyeasight
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Database Connection Strings (PostgreSQL)
CLOTHING_DB_URL="postgresql://user:password@hostname:5432/odoo_clothing"
FURNITURE_DB_URL="postgresql://user:password@hostname:5432/odoo_furniture"
RESTAURANT_DB_URL="postgresql://user:password@hostname:5432/odoo_restaurant"
```

#### 5. Download Data Sources

Place the Census data CSV in the `data/` folder:

- Download from: https://data.census.gov/table/ACSST5Y2024.S1101?g=860XX00US65054
- Files needed:
  - `ACSST5Y2024.S1902-Data.csv`
  - `ACSST5Y2024.S1902-Column-Metadata.csv`

### Server Deployment

For detailed server setup on Ubuntu, see [docs/OdooInstallation.md](docs/OdooInstallation.md)

```mermaid
flowchart TB
    Start@{shape: pill}

    PC["**Old Laptop** 💻<br/>
        - CPU: 2GHz Dual-Core<br/>
        - RAM: 8GB<br/>
        - Storage: 100GB<br/>
        - Ethernet/Wi-Fi<br/>
        - USB Port"]

    Start --> PC

    Ubuntu["**Ubuntu Server 24.04** 🐧<br/>
        - Rufus bootable USB<br/>
        - Enable UEFI boot<br/>
        - SSH enabled<br/>
        - WiFi configured"]
    PC --> Ubuntu

    Odoo["**Odoo Installation** 📦<br/>
        - PostgreSQL database<br/>
        - Odoo 17+ modules<br/>
        - Partner module sync"]
    Ubuntu --> Odoo

    style PC fill:#bbdefb
    style Ubuntu fill:#c8e6c9
    style Odoo fill:#ffe0b2
```

---

## Usage Guide

### Option 1: Interactive Streamlit Dashboard (Recommended)

The Streamlit app provides an interactive web interface:

```bash
# Activate virtual environment first
source venv/Scripts/activate  # Windows: venv\Scripts\activate
source venv/bin/activate      # macOS/Linux

# Run the dashboard
streamlit run streamlit_app.py
```

**Dashboard Features:**

- 🔍 **Test Database Connections**: Verify connectivity to all Odoo instances
- ⚡ **Load Cached Data**: Quick loading from processed parquet files
- 📊 **Force Refresh**: Re-geocode partners and update the map
- 🌍 **Interactive Map**: Zoom, pan, and explore partner locations
- 📥 **Data Export**: Download processed data in multiple formats

**Example Workflow:**

```
1. Open dashboard: http://localhost:8501
2. Click "Test Database Connections" to verify all DBs are reachable
3. Click "Use Cached Data" to load the latest partner map
4. Interact with the map: zoom into regions, click markers for details
5. Monitor the sidebar for data loading status
```

### Option 2: Python Script (Batch Processing)

For scheduled runs or data pipeline integration:

```bash
# Activate virtual environment
source venv/Scripts/activate

# Run the main script
python main.py
```

**What it does:**

1. Fetches partner data from all 3 Odoo databases
2. Geocodes addresses using Nominatim API (rate-limited)
3. Caches results to `data/partners_processed_coordinates.parquet`
4. Generates interactive map: `outputs/IKYEA_Partner_Map2.html`

**Output:**

```
📊 Database Connection Summary:
  I-Clothing: ✅ Loaded 542 partners
  I-Furniture: ✅ Loaded 387 partners
  I-Restaurant: ✅ Loaded 156 partners

💾 Cached processed coordinates to data/partners_processed_coordinates.parquet
🚀 Project Complete. Map saved to outputs/
```

### Example: Custom Data Processing

```python
from src.models.database import PartnerModel
from src.controllers.geo_controller import GeoController
from src.views.map_view import MapView
import os

# 1. Configure database connections
CONFIG = {
    'I-Clothing': os.getenv('CLOTHING_DB_URL'),
    'I-Furniture': os.getenv('FURNITURE_DB_URL'),
    'I-Restaurant': os.getenv('RESTAURANT_DB_URL')
}

# 2. Fetch data from all databases
model = PartnerModel(CONFIG)
df = model.fetch_all_data()
print(f"Loaded {len(df)} partners across all brands")

# 3. Geocode addresses
controller = GeoController()
df_processed = controller.process_coordinates(df)

# 4. Create visualization
view = MapView()
map_obj = view.render(df_processed)
map_obj.save("custom_map.html")
```

---

## Project Structure

```
ikyeasight/
├── main.py                          # Entry point for batch processing
├── streamlit_app.py                 # Streamlit dashboard application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── Queries.sql                      # Reference SQL queries
├── data/                            # Data storage
│   ├── ACSST5Y2024.S1902-Data.csv           # Census demographic data
│   ├── ACSST5Y2024.S1902-Column-Metadata.csv # Census column definitions
│   ├── ikyea_master_list.csv        # Master partner list
│   ├── ikyea_partners.csv           # Partner reference data
│   └── partners_processed_coordinates.parquet # Cached geocoded data
├── outputs/                         # Generated outputs
│   ├── IKYEA_Partner_Map2.html      # Interactive map (latest)
│   └── income_by_partner_location.html # Income analysis visualization
├── notebooks/                       # Jupyter notebooks & analysis
│   ├── partners_location.ipynb      # Partner mapping notebook v1
│   ├── partners_location_v2.ipynb   # Partner mapping notebook v2
│   ├── partners_geolocation.py      # Geolocation analysis script
│   ├── meanIncomePerPartnerLocation.py # Census income analysis
│   └── IKYEA_Partner_Map.html       # Generated map output
├── src/                             # Source code (MVC architecture)
│   ├── models/
│   │   ├── database.py              # PartnerModel: Database operations
│   │   └── queries.py               # SQL query constants
│   ├── controllers/
│   │   └── geo_controller.py        # GeoController: Geocoding logic
│   └── views/
│       └── map_view.py              # MapView: Folium visualization
└── docs/                            # Documentation
    ├── index.md                     # Project overview
    ├── OdooInstallation.md          # Server setup guide
    └── dev_nginx_dual_server_reverse_proxy.md # Nginx configuration
```

---

## Development Guide

### Adding a New Data Source

#### Step 1: Add Database URL

```bash
# .env file
NEW_BRAND_DB_URL="postgresql://user:pass@host/dbname"
```

#### Step 2: Update Configuration

```python
# streamlit_app.py or main.py
CONFIG = {
    'I-Clothing': os.getenv('CLOTHING_DB_URL'),
    'I-Furniture': os.getenv('FURNITURE_DB_URL'),
    'I-Restaurant': os.getenv('RESTAURANT_DB_URL'),
    'I-NewBrand': os.getenv('NEW_BRAND_DB_URL'),  # Add here
}
```

#### Step 3: Add Styling

```python
# src/views/map_view.py
self.brand_colors = {
    'I-Clothing': 'blue',
    'I-Furniture': 'green',
    'I-Restaurant': 'orange',
    'I-NewBrand': 'purple',  # Add here
    'Unknown': 'gray'
}
```

#### Step 4: Test Connection

```bash
streamlit run streamlit_app.py
# Click "Test Database Connections" to verify
```

### Customizing the Map

**Change Map Center and Zoom:**

```python
# src/views/map_view.py
m = folium.Map(
    location=[37.0902, -95.7129],  # Default: US center
    zoom_start=4,                   # Default: 4
    tiles='CartoDB voyager'         # Options: 'CartoDB positron', 'OpenStreetMap', etc.
)
```

**Modify Marker Appearance:**

```python
folium.Marker(
    location=[lat, lon],
    popup=partner_name,
    icon=folium.Icon(
        color='blue',           # Marker color
        icon='info-sign',      # Icon type
        prefix='fa'             # Font Awesome icons
    )
).add_to(marker_cluster)
```

### Performance Optimization

**Cache Management:**

- Processed data cached in Parquet format (fast I/O)
- Cache invalidated when force-refresh requested
- Located at: `data/partners_processed_coordinates.parquet`

**Geocoding Tips:**

- Uses Nominatim (1 request/second rate limit)
- Fallback strategy: full address → city+zip
- Consider caching coordinates in database

**Dashboard Optimization:**

- Streamlit caches components with `@st.cache_data`
- Database connections reused across page reloads
- Marker clustering reduces rendering overhead

### Running Tests

```bash
# Syntax check
python -m py_compile src/**/*.py

# Check imports
python -c "from src.models.database import PartnerModel; from src.controllers.geo_controller import GeoController; from src.views.map_view import MapView; print('✅ All imports OK')"

# Test database connection
python -c "from src.models.database import PartnerModel; import os; model = PartnerModel({k: os.getenv(f'{k.split('-')[1].upper()}_DB_URL') for k in ['I-Clothing', 'I-Furniture', 'I-Restaurant']}); print(model.fetch_all_data().head())"
```

### Code Style Guidelines

- **Python Version**: Python 3.9+
- **Formatting**: Follow PEP 8
- **Docstrings**: Include for all functions and classes
- **Type Hints**: Recommended for function parameters
- **Comments**: Explain complex logic (see existing code examples)

**Example Function:**

```python
def process_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Process and update coordinates in the DataFrame

    Args:
        df (pd.DataFrame): DataFrame with partner data including address fields

    Returns:
        pd.DataFrame: DataFrame with updated latitude and longitude columns
    """
    df['clean_address'] = df.apply(self.clean_address, axis=1)
    # ... rest of implementation
    return df
```

---

## Data Sources

### 1. Odoo Partner Database

**Source**: Odoo instances running across brand-specific deployments

- **I-Clothing**: I-Clothing Odoo instance
- **I-Furniture**: I-Furniture Odoo instance
- **I-Restaurant**: I-Restaurant Odoo instance

**Data Retrieved**:

```sql
SELECT p.name, p.street, p.city, p.zip,
       p.partner_latitude as lat, p.partner_longitude as lon,
       c.code as country_code
FROM res_partner p
LEFT JOIN res_country c ON p.country_id = c.id
WHERE p.active = True AND p.is_company = False;
```

**Update Frequency**: Real-time (on dashboard load)

### 2. U.S. Census Bureau - ACS 5-Year Estimates (2024)

**Source**: https://data.census.gov/table/ACSST5Y2024.S1101?g=860XX00US65054

**Data Included**:

- Household income by zip code
- Family income statistics
- Income by demographics (age, education, employment)

**Files Required**:

- `ACSST5Y2024.S1902-Data.csv` (Main dataset)
- `ACSST5Y2024.S1902-Column-Metadata.csv` (Column definitions)

**Update Frequency**: Annually

### 3. OpenStreetMap (via Nominatim)

**Service**: Nominatim Geospatial Database (OpenStreetMap)

**Purpose**: Geocoding (address → latitude/longitude conversion)

**Rate Limits**: 1 request/second (enforced by geopy.extra.rate_limiter)

**Fallback**: If full address fails, attempts city+zip only

---

## Troubleshooting

### Database Connection Issues

**Problem**: ❌ Database unreachable error

```
Error fetching I-Clothing: (psycopg2.OperationalError) could not connect to server: Connection timed out
```

**Solution**:

1. Verify connection string format: `postgresql://user:password@host:port/dbname`
2. Check host is reachable: `ping hostname`
3. Verify credentials: `psql -U user -d dbname -h host`
4. Check firewall: Allow port 5432 (PostgreSQL default)
5. Test in Streamlit dashboard: Click "Test Database Connections"

### Geocoding Issues

**Problem**: Addresses not being geocoded (lat/lon remain 0)

```
pd.Series(['clean_address']=0  # latitude not updated
```

**Solution**:

1. Check internet connection (Nominatim requires HTTP access)
2. Verify address format (street, city, zip, country code)
3. Test manually:
   ```python
   from geopy.geocoders import Nominatim
   geolocator = Nominatim(user_agent="test")
   location = geolocator.geocode("123 Main St, Springfield, 65000, US")
   print(location)
   ```
4. Check rate limit (1 request/second) - reduce concurrent requests
5. Use fallback strategy (city+zip only)

### Streamlit Dashboard Issues

**Problem**: Dashboard won't start

```
StreamlitAPIException: Secrets not found
```

**Solution**:

1. Create `.streamlit/secrets.toml`:
   ```toml
   DB_CLOTHING="postgresql://..."
   DB_FURNITURE="postgresql://..."
   DB_RESTAURANT="postgresql://..."
   ```
2. Or use environment variables: `export DB_CLOTHING="..."`
3. Restart Streamlit: `streamlit run streamlit_app.py`

**Problem**: Map not displaying

```
folium.exceptions.PluginException: branca not installed
```

**Solution**: Install dependencies again

```bash
pip install -r requirements.txt --force-reinstall
streamlit run streamlit_app.py
```

### Performance Issues

**Problem**: Dashboard slow or freezing

**Solution**:

1. Use cached data: Click "Use Cached Data" button
2. Check cache size: `ls -lh data/partners_processed_coordinates.parquet`
3. Clear cache and rebuild:
   ```bash
   rm data/partners_processed_coordinates.parquet
   python main.py  # Rebuild cache
   ```
4. Monitor resource usage: `top` (Linux) or Task Manager (Windows)

---

## Infrastructure Setup

Complete server deployment guide available in [docs/OdooInstallation.md](docs/OdooInstallation.md)

### Quick Start: Local Development

```bash
# 1. Clone and setup
git clone https://github.com/otalfredo8/ikyeasight.git
cd ikyeasight
python -m venv venv
source venv/Scripts/activate

# 2. Install and configure
pip install -r requirements.txt
# Create .env with database URLs / set environment variables

# 3. Run dashboard
streamlit run streamlit_app.py
# Opens at http://localhost:8501
```

### Production Deployment

See [docs/dev_nginx_dual_server_reverse_proxy.md](docs/dev_nginx_dual_server_reverse_proxy.md) for:

- Nginx reverse proxy configuration
- SSL/TLS setup
- Load balancing across multiple servers
- Docker containerization (if applicable)

---

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes following code style guidelines
3. Test locally: `streamlit run streamlit_app.py`
4. Commit: `git commit -m "Add feature description"`
5. Push: `git push origin feature/your-feature`
6. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Support & Contact

For questions or issues:

- 📧 Email: [Project Contact]
- 🐛 Issues: [GitHub Issues](https://github.com/otalfredo8/ikyeasight/issues)
- 📖 Documentation: See `docs/` folder

---

**Last Updated**: April 2026  
**Current Version**: 1.0.0
come, family income, and income by demographics
