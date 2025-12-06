import get_data
import save_to_database
import os
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import alert
import analyzer

# get variable from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

# cities's list 
CITIES = [
    "Hanoi", 
    "Ho Chi Minh City", 
    "Da Nang", 
    "Seoul", 
    "Tokyo", 
    "London", 
    "New York", 
    "Bangkok", "Chiang Mai",     
    "Singapore",                  
    "Kuala Lumpur",               
    "Jakarta", "Bali",            
    "Manila",                     
    "Phnom Penh",                
    "Vientiane",                  
    "Yangon",                     
    "Osaka", "Kyoto",    
    "Busan",             
    "Beijing", "Shanghai", "Guangzhou", "Shenzhen", 
    "Hong Kong", "Macau",         
    "Taipei",                    
    "New Delhi", "Mumbai", "Bangalore",
    "Dhaka",                      
    "Colombo",                    
    "Kathmandu",                  
    "Islamabad", "Karachi"      
]

def handling_data(city_name):
    try:
        cleaned_data = get_data.transform_data(city_name,API_KEY)
        # data handling
        if cleaned_data:
            # save data block
            save_to_database.save_log(cleaned_data, DB_CONNECTION_STRING)
            print("Successful saving")
                    
            # alert block for ha noi weather
            if(city_name == 'Hanoi'):
                warning_msg = alert.alert_condition(cleaned_data)
                air_alert = analyzer.air_condition(cleaned_data['pm2_5_index'])
                temp_alert = analyzer.feeling(cleaned_data['temperature'], cleaned_data['humidity'])
                warning_msg += f'The air condition is {air_alert}\n'
                warning_msg += f"Feeling like {temp_alert[0]} and {temp_alert[1]}"
                alert.send_message_to_devices(warning_msg)

        else:
            print("Failed to saving to the data")
    except Exception as e:
        print(f"   [ERROR] Lỗi tại {city_name}: {e}")
        return

def main():
    # check api key
    if not API_KEY:
        print('Missing API key')
        return
    # check database connection
    if not DB_CONNECTION_STRING:
        print('Missing DB connection string')
        return
    
    # multithreading for calling API
    with ThreadPoolExecutor(max_workers=5) as executor:
        # futures = {executor.submit(handling_data, city_name): city_name for city_name in CITIES}

        # for future in as_completed(futures):
        #     city_name = futures[future] 
        #     try:
        #         result = future.result() 
        #     except Exception as exc:
        #         print(f'❌ {city_name} bị lỗi: {exc}')
        for city in CITIES:
            executor.submit(handling_data,city)
    
    print('swepping data successful')

# start point of programming
if __name__ == "__main__":
    main()