import pandas as pd
from sqlalchemy import create_engine
from .queries import GET_PARTNERS

class PartnerModel:
    def __init__(self, config):
        self.config = config
        self.query = GET_PARTNERS # sql query to fetch partner data

    def fetch_all_data(self):
        all_data = []
        for brand, conn_str in self.config.items():
            try:
                engine = create_engine(conn_str) # db_driver://user:pass@host/dbname
                df_temp = pd.read_sql(self.query, engine) 
                df_temp['brand'] = brand
                all_data.append(df_temp) # append all rows per query and brand
            except Exception as e:
                print(f"Error fetching {brand}: {e}")
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame() # ternary operator