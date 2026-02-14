from fastapi import FastAPI, HTTPException
from database import DatabaseManager
from logger import setup_logger
from config import Config

logger = setup_logger(__name__)
app = FastAPI()

# Initialize database manager
try:
    db_manager = DatabaseManager(Config.DB_CONNECTION_STRING)
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")

@app.get("/cities")
def read_cities():
    """Get list of all cities with weather data"""
    try:
        cities = db_manager.get_distinct_cities()
        logger.info(f"Retrieved {len(cities)} cities")
        return cities
    except Exception as e:
        logger.error(f"Error fetching cities: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/weather/{city_name}")
def get_weather_for_city(city_name: str):
    """Get weather data for a specific city (SQL injection safe)"""
    if not city_name or len(city_name) < 2:
        raise HTTPException(status_code=400, detail="Invalid city name")
    
    try:
        weather_data = db_manager.get_city_weather(city_name)
        logger.info(f"Retrieved weather data for {city_name}")
        return weather_data
    except Exception as e:
        logger.error(f"Error fetching weather for {city_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}