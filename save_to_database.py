import get_data
import pandas as pd
from sqlalchemy import create_engine



def save_log(dict_data,  db_connection_string, table_name = 'weather_logs'):
    
    if not dict_data:
        print("No data for saving")
        return
    
    # save to database
    try:
        ENGINE = create_engine(db_connection_string)
        data_frame = pd.DataFrame([dict_data])

        data_frame.to_sql(
            name = table_name,
            con=ENGINE,
            if_exists = 'append',
            index = False
        )
        print(f'Saving to table sucessful')
    except Exception as e:
        print(f'Error while saving to database: {e}')
