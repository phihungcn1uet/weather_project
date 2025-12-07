from fastapi import FastAPI
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd

app = FastAPI()

# database connection string
load_dotenv()
db_connection_string = os.getenv('DB_CONNECTION_STRING')

engine = create_engine(db_connection_string)

@app.get("/cities")
def read_city():
    try: 
        query = "SELECT DISTINCT city FROM weather_logs"
        df = pd.read_sql(query,engine)
        return df['city'].to_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi DB: {str(e)}")

@app.get("/weather/{city_name}")
def get_weather_for_each_city(city_name : str):
    try:
        query = f"SELECT * FROM weather_logs WHERE city = '{city_name}'"
        df = pd.read_sql(query,engine)
        return df.to_dict(orient = 'records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi DB: {str(e)}")
