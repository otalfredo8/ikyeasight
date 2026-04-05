import folium
from folium.plugins import MarkerCluster
import pandas as pd

class MapView:
    def __init__(self):
        self.brand_colors = {
            'I-Clothing': 'blue', 
            'I-Furniture': 'green',
            'I-Restaurant': 'orange', 
            'Unknown': 'gray'
        }

    def render(self, df):
        """
        Render map with clustered markers
        Args:
            df (pd.DataFrame):DataFrame with partner data (name, lat, lon, brand)
        Returns:
            folium.Map: Interactive map object with clustered markers
        """
        m = folium.Map(location=[37.0902, -95.7129], 
                       zoom_start=4, tiles='CartoDB voyager') # Create and center map on US coordinates
        
        marker_cluster = MarkerCluster().add_to(m) # clustered markers
        
        for _, row in df.iterrows():
            if row['lat'] != 0 and pd.notnull(row['lat']):
                # createa a marker using named parameters rather than positional
                folium.Marker( 
                    location=[row['lat'], row['lon']],
                    popup=row['name'],
                    # named parameters rather than positional
                    icon=folium.Icon(color=self.brand_colors.get(row['brand'], 'gray'))
                ).add_to(marker_cluster)
        return m