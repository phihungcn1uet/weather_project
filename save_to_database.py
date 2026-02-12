from database import DatabaseManager
from logger import setup_logger
from exceptions import DatabaseError
from validators import DataValidator

logger = setup_logger(__name__)

def save_log(dict_data: dict, db_connection_string: str, table_name: str = 'weather_logs') -> bool:
    """Save weather data to database"""
    if not dict_data:
        logger.warning("No data provided for saving")
        return False
    
    # Validate data before saving
    is_valid, msg = DataValidator.validate_weather_data(dict_data)
    if not is_valid:
        logger.error(f"Data validation failed: {msg}")
        return False
    
    try:
        db_manager = DatabaseManager(db_connection_string)
        success = db_manager.save_data(dict_data, table_name)
        if success:
            logger.info(f"Data saved successfully to {table_name}")
        return success
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while saving: {e}")
        return False