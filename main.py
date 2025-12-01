import get_data
import save_to_database
import os
from dotenv import load_dotenv
import alert
import analyzer

# get variable from .env file
load_dotenv()
CITY_NAME = os.getenv('CITY_NAME')
API_KEY = os.getenv('API_KEY')
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")


def main():
    # check api key
    if not API_KEY:
        print('Missing API key')
        return
    # check database connection
    if not DB_CONNECTION_STRING:
        print('Missing DB connection string')
        return
    
    # call data
    cleaned_data = get_data.transform_data(CITY_NAME,API_KEY)

    # data handling
    if cleaned_data:
        # save data block
        # save_to_database.save_log(cleaned_data, DB_CONNECTION_STRING)
        print("Successful saving")
        # alert block
        warning_msg = alert.alert_condition(cleaned_data)
        air_alert = analyzer.air_condition(cleaned_data['pm2_5_index'])
        temp_alert = analyzer.feeling(cleaned_data['temperature'], cleaned_data['humidity'])
        warning_msg += f'The air condition is {air_alert}\n'
        warning_msg += f"Felling like {temp_alert[0]} and {temp_alert[1]}"
        alert.send_message_to_devices(warning_msg)

    else:
        print("Failed to saving to the data")

# start point of programming
if __name__ == "__main__":
    main()