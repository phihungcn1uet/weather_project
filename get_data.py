import requests
import json
# time function
from datetime import datetime


# call API function
def extract_weather_data(city_name, api_key):
    # weather URL
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    try:
        response = requests.get(URL)
        response.raise_for_status() # throw exception
        print('API Connection Sucessful')
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'API Connection Failed:{e}')
        return None


# pollutioin data collection through location
def extract_pollution_data(lat, lon, api_key):

    # pollution URL
    pollution_URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
  
    try:
        response = requests.get(pollution_URL)
        response.raise_for_status() # determine status
        print('Pollution Data API Connection Sucessful')
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Pollution Data API Connection Failed:{e}')
        return None

# collect data
def transform_data(city_name, api_key):
    
    data = extract_weather_data(city_name, api_key)

    # coordinate of the city
    lat = data['coord']['lat']
    lon = data['coord']['lon']

    # use the coordinate to get pollution data
    data_pollution = extract_pollution_data(lat,lon,api_key)
    try:
        cleaned_data = {
            #normal data
            "time" : unix_to_real_time(data['dt']),
            "weather" : data['weather'][0]['main'],
            "description" : data['weather'][0]['description'],
            "temperature" : kelvin_to_celsius(data['main']['temp']),
            "humidity" : data['main']['humidity'],

            #air data
            "aqi_index" : data_pollution['list'][0]['main']['aqi'],
            "CO_index" : data_pollution ['list'][0]['components']['co'],
            "NO2_index" : data_pollution ['list'][0]['components']['no2'],
            "O3_index ": data_pollution ['list'][0]['components']['o3'],
            "pm2_5_index" : data_pollution ['list'][0]['components']['pm2_5'],
            "pm10_index" : data_pollution ['list'][0]['components']['pm10']
        }

        return cleaned_data
    except KeyError as e:
        print(f"Error while cleaning JSON data: Key {e} missing")
        return None

# convert function
def kelvin_to_celsius(kelvin_temp):
        celsius_temp = kelvin_temp - 273.15
        return celsius_temp

def unix_to_real_time(unix_time):
        local_time = datetime.fromtimestamp(unix_time)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')