from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

class GeoController:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="ikyea_mapper", timeout=10)
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)

    def clean_address(self, row):
        street = str(row['street']).strip()
        country = row['country_code'] if pd.notnull(row['country_code']) else 'US'
        if street in ['NULL', 'None', 'nan', ''] or row['street'] is None: # no street no problem
            return f"{row['city']}, {row['zip']}, {country}"
        return f"{street}, {row['city']}, {row['zip']}, {country}" # single formated address string

    def process_coordinates(self, df):
        df['clean_address'] = df.apply(self.clean_address, axis=1) # to clean_address column add a cleaned address row by row
        for index, row in df.iterrows():
            if row['lat'] == 0 or pd.isnull(row['lat']):
                location = self.geocode(row['clean_address']) # geopy location generates lat and lon from full clean address
                if not location:
                    location = self.geocode(f"{row['city']}, {row['zip']}") # geopy location generates lat and lon from zip and city only
                
                if location:
                    df.at[index, 'lat'] = location.latitude # update lat column in the current row (index)
                    df.at[index, 'lon'] = location.longitude # update lon column in the current row (index)
        return df