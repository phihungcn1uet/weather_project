import get_data
import save_to_database
import os
from dotenv import load_dotenv

# get variable from .env file
load_dotenv()
CITY_NAME = os.getenv('CITY_NAME')
API_KEY = os.getenv('API_KEY')
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

def main():
    # check api key
    if not API_KEY:
        print('Can not find API key from .env file')
        return

    # call data
    data = get_data.transform_data(CITY_NAME,API_KEY)

    # save to database
    if data:
        save_to_database.save_log(data, DB_CONNECTION_STRING)
        print("Successful saving")
    else:
        print("Failed to saving to the data")

# start point of programming
if __name__ == "__main__":
    main()