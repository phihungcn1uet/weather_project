from notifications import NotificationManager
from analyzer import air_condition, feeling
from logger import setup_logger
from config import Config

logger = setup_logger(__name__)

def send_alert(data: dict) -> bool:
    """Send weather alert via Telegram"""
    try:
        notifier = NotificationManager(Config.TELEGRAM_TOKEN, Config.TELEGRAM_CHAT_ID)
        return notifier.send_alert(data)
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")
        return False

def format_alert_message(data: dict) -> str:
    """Format detailed alert message with analysis"""
    try:
        air_qual = air_condition(data['pm2_5_index'])
        temp_feel, humidity_feel = feeling(data['temperature'], data['humidity'])
        
        message = f"*⚠️ Weather Alert - {data['city']}*\n"
        message += f"📍 Time: {data['time']}\n\n"
        message += f"🌡️ Temperature: {data['temperature']}°C (feels {temp_feel})\n"
        message += f"💧 Humidity: {data['humidity']}% ({humidity_feel})\n"
        message += f"☁️ Weather: {data['weather']} - {data['description']}\n\n"
        message += f"*🌫️ Air Quality:*\n"
        message += f"├ AQI Index: {data['aqi_index']}\n"
        message += f"├ PM2.5: {data['pm2_5_index']}µg/m³ ({air_qual})\n"
        message += f"├ PM10: {data['pm10_index']}µg/m³\n"
        message += f"├ NO₂: {data['NO2_index']}µg/m³\n"
        message += f"└ O₃: {data['O3_index']}µg/m³\n"
        
        return message
    except Exception as e:
        logger.error(f"Error formatting alert message: {e}")
        return "Weather Alert - Unable to format message"

def send_detailed_alert(data: dict) -> bool:
    """Send detailed weather alert"""
    try:
        message = format_alert_message(data)
        notifier = NotificationManager(Config.TELEGRAM_TOKEN, Config.TELEGRAM_CHAT_ID)
        return notifier.send_message(message)
    except Exception as e:
        logger.error(f"Failed to send detailed alert: {e}")
        return False