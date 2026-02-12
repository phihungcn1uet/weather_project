import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Config:
    # API Configuration
    API_KEY = os.getenv('API_KEY')
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    REQUEST_TIMEOUT = 10
    
    # Database Configuration
    DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
    DB_TABLE_NAME = 'weather_logs'
    
    # Telegram Configuration
    TELEGRAM_TOKEN = os.getenv('TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')
    
    # Threading Configuration
    MAX_WORKERS = 5
    
    # Cities List
    CITIES: List[str] = [
        "Hanoi", "Ho Chi Minh City", "Da Nang", "Seoul", "Tokyo",
        "London", "New York", "Bangkok", "Chiang Mai", "Singapore",
        "Kuala Lumpur", "Jakarta", "Bali", "Manila", "Phnom Penh",
        "Vientiane", "Yangon", "Osaka", "Kyoto", "Busan",
        "Beijing", "Shanghai", "Guangzhou", "Shenzhen",
        "Hong Kong", "Macau", "Taipei",
        "New Delhi", "Mumbai", "Bangalore", "Dhaka", "Colombo",
        "Kathmandu", "Islamabad", "Karachi"
    ]
    
    @staticmethod
    def validate():
        """Validate all required configurations"""
        errors = []
        if not Config.API_KEY:
            errors.append("Missing API_KEY")
        if not Config.DB_CONNECTION_STRING:
            errors.append("Missing DB_CONNECTION_STRING")
        if not Config.TELEGRAM_TOKEN:
            errors.append("Missing TELEGRAM_TOKEN")
        if not Config.TELEGRAM_CHAT_ID:
            errors.append("Missing TELEGRAM_CHAT_ID")
        return errors