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
        # Center map on average lat/lon
        m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], 
                       zoom_start=5, tiles='CartoDB positron')
        
        marker_cluster = MarkerCluster().add_to(m)
        
        for _, row in df.iterrows():
            if row['lat'] != 0 and pd.notnull(row['lat']):
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=row['name'],
                    icon=folium.Icon(color=self.brand_colors.get(row['brand'], 'gray'))
                ).add_to(marker_cluster)
        return m