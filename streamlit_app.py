import streamlit as st
from streamlit_folium import st_folium
from src.models.database import PartnerModel
from src.controllers.geo_controller import GeoController
from src.views.map_view import MapView

# Page Configuration
st.set_page_config(page_title="IKYEASight Dashboard", layout="wide")

# 1. Setup Configuration (In a real app, use st.secrets for passwords!)
CONFIG = {
    'I-Clothing': 'postgresql://odoo:Admin123Admin123@192.168.1.249:5432/odoo19_bat_dev',
    'I-Furniture': 'postgresql://odoo:userodoo123@23.122.200.31:5432/odoo_stg',
    'I-Restaurant': 'postgresql://odoo:Admin123Admin123@34.63.102.13:5432/odoo19_gc_db' 
}

st.title("🌍 IKYEASight: Global Partner Mapper")
st.markdown("This dashboard pulls live data from Odoo and maps partner locations.")

# Initialize our MVC Components
model = PartnerModel(CONFIG)
controller = GeoController()
view = MapView()

# Sidebar for controls
with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Sync & Geocode Data"):
        with st.spinner("Fetching data from Odoo and calculating coordinates..."):
            # EXECUTE MVC FLOW
            df_raw = model.fetch_all_data()
            df_processed = controller.process_coordinates(df_raw)
            
            # Save to session state so it doesn't disappear on refresh
            st.session_state['data'] = df_processed
            st.success(f"Loaded {len(df_processed)} partners!")

# Main Display Logic
if 'data' in st.session_state:
    df = st.session_state['data']
    
    # Create the Map via View
    map_obj = view.render(df)
    
    # Display the Map
    st_folium(map_obj, width=1200, height=600)
    
    # Show Raw Data Table below
    with st.expander("See Raw Partner Data"):
        st.dataframe(df)
else:
    st.info("Click the 'Sync & Geocode Data' button in the sidebar to start.")