import requests
from datetime import datetime
from logger import setup_logger
from exceptions import WeatherAPIError, PollutionAPIError
from validators import DataValidator
from retry import retry_with_backoff
from config import Config

logger = setup_logger(__name__)

@retry_with_backoff(max_attempts=3, initial_delay=2)
def extract_weather_data(city_name: str, api_key: str) -> dict:
    """Fetch weather data from OpenWeatherMap API"""
    is_valid, msg = DataValidator.validate_city_name(city_name)
    if not is_valid:
        raise WeatherAPIError(msg)
    
    url = f"{Config.OPENWEATHER_BASE_URL}/weather?q={city_name}&appid={api_key}"
    
    try:
        response = requests.get(url, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        is_valid, msg = DataValidator.validate_api_response(data, "weather")
        if not is_valid:
            raise WeatherAPIError(msg)
        
        logger.info(f'Weather data fetched for {city_name}')
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f'Weather API failed for {city_name}: {e}')
        raise WeatherAPIError(f"Failed to fetch weather data: {e}")

@retry_with_backoff(max_attempts=3, initial_delay=2)
def extract_pollution_data(lat: float, lon: float, api_key: str) -> dict:
    """Fetch pollution data from OpenWeatherMap API"""
    url = f"{Config.OPENWEATHER_BASE_URL}/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    
    try:
        response = requests.get(url, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        is_valid, msg = DataValidator.validate_api_response(data, "pollution")
        if not is_valid:
            raise PollutionAPIError(msg)
        
        logger.info(f'Pollution data fetched for lat={lat}, lon={lon}')
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f'Pollution API failed: {e}')
        raise PollutionAPIError(f"Failed to fetch pollution data: {e}")

def transform_data(city_name: str, api_key: str) -> dict:
    """Transform and combine weather and pollution data"""
    try:
        weather_data = extract_weather_data(city_name, api_key)
        
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']
        
        pollution_data = extract_pollution_data(lat, lon, api_key)
        
        cleaned_data = {
            "lat": lat,
            "lon": lon,
            "city": city_name,
            "time": unix_to_real_time(weather_data['dt']),
            "weather": weather_data['weather'][0]['main'],
            "description": weather_data['weather'][0]['description'],
            "temperature": kelvin_to_celsius(weather_data['main']['temp']),
            "humidity": weather_data['main']['humidity'],
            "aqi_index": pollution_data['list'][0]['main']['aqi'],
            "CO_index": pollution_data['list'][0]['components']['co'],
            "NO2_index": pollution_data['list'][0]['components']['no2'],
            "O3_index": pollution_data['list'][0]['components']['o3'],
            "pm2_5_index": pollution_data['list'][0]['components']['pm2_5'],
            "pm10_index": pollution_data['list'][0]['components']['pm10']
        }
        
        is_valid, msg = DataValidator.validate_weather_data(cleaned_data)
        if not is_valid:
            logger.error(f"Data validation failed: {msg}")
            return None
        
        logger.info(f'Data transformed successfully for {city_name}')
        return cleaned_data
    
    except (WeatherAPIError, PollutionAPIError) as e:
        logger.error(f"Error transforming data for {city_name}: {e}")
        return None
    except KeyError as e:
        logger.error(f"Missing key in API response: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

def kelvin_to_celsius(kelvin_temp: float) -> float:
    """Convert temperature from Kelvin to Celsius"""
    return round(kelvin_temp - 273.15, 2)

def unix_to_real_time(unix_time: int) -> str:
    """Convert Unix timestamp to readable format"""
    local_time = datetime.fromtimestamp(unix_time)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')