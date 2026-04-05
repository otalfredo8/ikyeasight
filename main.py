import os
from src.models.database import PartnerModel
from src.controllers.geo_controller import GeoController
from src.views.map_view import MapView

CONFIG = {
    'I-Clothing': os.getenv('CLOTHING_DB_URL'),
    'I-Furniture': os.getenv('FURNITURE_DB_URL'),
    'I-Restaurant': os.getenv('RESTAURANT_DB_URL')
}

def main():
    # 1. MODEL: Get Data
    model = PartnerModel(CONFIG)
    df = model.fetch_all_data()

    # 2. CONTROLLER: Process Data
    controller = GeoController()
    df_processed = controller.process_coordinates(df)

    # 3. CACHE: Save processed data to avoid re-geocoding
    if not os.path.exists("data"): os.makedirs("data")
    df_processed.to_parquet("data/partners_processed_coordinates.parquet", index=False)
    print("💾 Cached processed coordinates to data/partners_processed_coordinates.parquet")

    # 4. VIEW: Create Visual
    view = MapView()
    map_obj = view.render(df_processed)

    # Output Logic
    if not os.path.exists("outputs"): os.makedirs("outputs")
    map_obj.save("outputs/IKYEA_Partner_Map2.html")
    print("🚀 Project Complete. Map saved to outputs/")

if __name__ == "__main__":
    main()