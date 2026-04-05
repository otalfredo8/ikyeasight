import pandas as pd
from sqlalchemy import create_engine
from .queries import GET_PARTNERS

class PartnerModel:

    def __init__(self, config):
        self.config = config
        self.query = GET_PARTNERS # sql query to fetch partner data

    def fetch_all_data(self, verbose=True):
        """
        Fetch partner data from all brand databases
        Returns:
            pd.DataFrame: Combined DataFrame with partner data from all brands
        """
        all_data = []
        results = {}
        for brand, conn_str in self.config.items():
            try:
                engine = create_engine(conn_str) # db_driver://user:pass@host/dbname
                df_temp = pd.read_sql(self.query, engine) 
                df_temp['brand'] = brand
                all_data.append(df_temp) # append all rows per query and brand
                results[brand] = f"✅ Loaded {len(df_temp)} partners"
            except Exception as e:
                results[brand] = f"❌ FAILED: {str(e)}"
                if verbose:
                    print(f"Error fetching {brand}: {e}")
        
        # Print summary regardless of verbose flag
        print("\n📊 Database Connection Summary:")
        for brand, status in results.items():
            print(f"  {brand}: {status}")
        
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame() # ternary operator