---
layout: page
title: API Reference
permalink: /api-reference/
---

# API Reference

This page documents all public classes and methods in the `src/` package.

---

## `src.models.database` — `PartnerModel`

Fetches partner data from multiple Odoo PostgreSQL databases.

### Constructor

```python
PartnerModel(config: dict)
```

| Parameter | Type | Description |
|---|---|---|
| `config` | `dict` | Mapping of `brand_name → postgresql_connection_string` |

**Example:**
```python
config = {
    'I-Clothing':   'postgresql://user:pass@host:5432/db',
    'I-Furniture':  'postgresql://user:pass@host:5432/db',
    'I-Restaurant': 'postgresql://user:pass@host:5432/db',
}
model = PartnerModel(config)
```

---

### `fetch_all_data`

```python
fetch_all_data(verbose: bool = True) -> pd.DataFrame
```

Connects to each database in `config`, executes `GET_PARTNERS`, and returns a single combined DataFrame.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `verbose` | `bool` | `True` | Print per-brand errors to stdout |

**Returns:** `pd.DataFrame` with columns: `name`, `street`, `city`, `zip`, `lat`, `lon`, `country_code`, `brand`

**Behavior:**
- Skips unreachable databases (logs the error) and continues with others
- Appends a `brand` column to identify the source database
- Returns an empty DataFrame if all connections fail

---

## `src.models.queries` — SQL Constants

### `GET_PARTNERS`

SQL string that fetches active, non-company partners with their address and coordinate fields.

```sql
SELECT p.name, p.street, p.city, p.zip,
       p.partner_latitude  AS lat,
       p.partner_longitude AS lon,
       c.code              AS country_code
FROM   res_partner p
LEFT JOIN res_country c ON p.country_id = c.id
WHERE  p.active     = True
  AND  p.is_company = False;
```

---

## `src.controllers.geo_controller` — `GeoController`

Geocodes partner addresses using the Nominatim (OpenStreetMap) API.

### Constructor

```python
GeoController()
```

Initializes a `Nominatim` geolocator with:
- `user_agent="ikyea_mapper"`
- `timeout=10` seconds
- `RateLimiter` with 1-second minimum delay between requests

---

### `clean_address`

```python
clean_address(row: pd.Series) -> str
```

Formats a DataFrame row into a geocoding-friendly address string.

| Parameter | Type | Description |
|---|---|---|
| `row` | `pd.Series` | Row with fields: `street`, `city`, `zip`, `country_code` |

**Returns:** `str` — e.g. `"123 Main St, Springfield, 62701, US"` or `"Springfield, 62701, US"` if no street

---

### `process_coordinates`

```python
process_coordinates(df: pd.DataFrame) -> pd.DataFrame
```

Geocodes all rows in `df` that have missing or zero coordinates.

| Parameter | Type | Description |
|---|---|---|
| `df` | `pd.DataFrame` | DataFrame with partner data including address columns |

**Returns:** `pd.DataFrame` — same DataFrame with `lat` and `lon` columns updated

**Behavior:**
- Skips rows where `lat` is already non-zero
- Falls back to `"city, zip"` geocoding if full-address lookup fails
- Rows that cannot be geocoded retain their original (zero) coordinates

---

## `src.views.map_view` — `MapView`

Renders an interactive Folium map with brand-colored, clustered markers.

### Constructor

```python
MapView()
```

Initializes brand color mapping:

| Brand | Marker Color |
|---|---|
| `I-Clothing` | blue |
| `I-Furniture` | green |
| `I-Restaurant` | orange |
| _(unknown)_ | gray |

---

### `render`

```python
render(df: pd.DataFrame) -> folium.Map
```

Creates a Folium map and adds a clustered marker for each partner with valid coordinates.

| Parameter | Type | Description |
|---|---|---|
| `df` | `pd.DataFrame` | DataFrame with columns: `name`, `lat`, `lon`, `brand` |

**Returns:** `folium.Map` — interactive map object centered on the continental US (zoom level 4)

**Behavior:**
- Skips rows where `lat` is zero or null
- Groups markers using `MarkerCluster` to avoid clutter at low zoom levels
- Popups display the partner's `name`
