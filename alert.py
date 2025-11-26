import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")
chat_id = os.getenv("CHAT_ID")

# sending function
def send_message_to_devices(message):
    if not token or not chat_id:
        print("Wrong telegram token or chat id")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown" 
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Send alert to Telegram successful")
        else:
            print(f'Failed to send alert:{response.text}')
    except Exception as e:
        print(f'Error while connecting to Telegram:{e}')

# alert condition
def alert_condition(data):
    time = data['time']
    pm25 = data['pm2_5_index']
    temp = data['temperature']
    air_quality = data['aqi_index']
    warning_msg =f"At {time}\n"
    warning_msg +=f"The air quality index is {air_quality}\n"
    warning_msg += f"The PM2.5 dust index is {pm25}\n"
    warning_msg += f"The temperature is {temp}\n"

    return warning_msg

