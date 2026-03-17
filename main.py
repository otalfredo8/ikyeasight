import os
from src.models.database import PartnerModel
from src.controllers.geo_controller import GeoController
from src.views.map_view import MapView

CONFIG = {
    'I-Clothing': 'postgresql://odoo:Admin123Admin123@192.168.1.249:5432/odoo19_bat_dev',
    'I-Furniture': 'postgresql://odoo:userodoo123@23.122.200.31:5432/odoo_stg',
    'I-Restaurant': 'postgresql://odoo:Admin123Admin123@136.112.69.211:5432/odoo19_gc_db'
}

def main():
    # 1. MODEL: Get Data
    model = PartnerModel(CONFIG)
    df = model.fetch_all_data()

    # 2. CONTROLLER: Process Data
    controller = GeoController()
    df_processed = controller.process_coordinates(df)

    # 3. VIEW: Create Visual
    view = MapView()
    map_obj = view.render(df_processed)

    # Output Logic
    if not os.path.exists("outputs"): os.makedirs("outputs")
    map_obj.save("outputs/IKYEA_Partner_Map2.html")
    print("🚀 Project Complete. Map saved to outputs/")

if __name__ == "__main__":
    main()