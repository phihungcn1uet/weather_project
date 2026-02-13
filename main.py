import get_data
import save_to_database
import alert
from concurrent.futures import ThreadPoolExecutor, as_completed
from logger import setup_logger
from config import Config
from metrics import MetricsCollector
from exceptions import ConfigError

logger = setup_logger(__name__)
metrics = MetricsCollector()

def handle_city_data(city_name: str) -> dict:
    """Process weather data for a single city"""
    try:
        logger.info(f"Processing data for {city_name}")
        metrics.record_api_call()
        
        # Fetch and transform data
        cleaned_data = get_data.transform_data(city_name, Config.API_KEY)
        
        if not cleaned_data:
            logger.warning(f"No data received for {city_name}")
            metrics.record_save(False)
            return {"city": city_name, "status": "failed", "reason": "No data"}
        
        # Save to database
        success = save_to_database.save_log(cleaned_data, Config.DB_CONNECTION_STRING)
        metrics.record_save(success)
        
        if not success:
            return {"city": city_name, "status": "failed", "reason": "Save failed"}
        
        # Send alert for Hanoi
        if city_name.lower() == 'hanoi':
            alert.send_detailed_alert(cleaned_data)
        
        logger.info(f"Successfully processed {city_name}")
        return {"city": city_name, "status": "success"}
    
    except Exception as e:
        logger.error(f"Error processing {city_name}: {e}")
        metrics.record_error(f"{city_name}: {str(e)}")
        metrics.record_save(False)
        return {"city": city_name, "status": "error", "reason": str(e)}

def main():
    """Main execution function"""
    logger.info("Starting weather data collection")
    
    # Validate configuration
    config_errors = Config.validate()
    if config_errors:
        error_msg = "Configuration errors: " + ", ".join(config_errors)
        logger.error(error_msg)
        raise ConfigError(error_msg)
    
    results = []
    
    # Process cities with multithreading
    with ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
        futures = {
            executor.submit(handle_city_data, city): city 
            for city in Config.CITIES
        }
        
        for future in as_completed(futures):
            city_name = futures[future]
            try:
                result = future.result()
                results.append(result)
                status = result.get('status', 'unknown')
                logger.info(f"{city_name}: {status}")
            except Exception as e:
                logger.error(f"Unexpected error for {city_name}: {e}")
                results.append({"city": city_name, "status": "error", "reason": str(e)})
    
    # Print metrics report
    report = metrics.get_report()
    logger.info(f"Collection complete. Success rate: {report['success_rate']:.2f}%")
    logger.info(f"Results summary: {len([r for r in results if r['status'] == 'success'])}/{len(Config.CITIES)} successful")
    
    return results

if __name__ == "__main__":
    try:
        results = main()
        logger.info("Weather data collection completed successfully")
    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)