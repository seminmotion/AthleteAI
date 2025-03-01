import os
import base64
import json
from typing import List

class Config:
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # Twitter (Optional)
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "").replace(
        "postgres://", "postgresql+asyncpg://", 1
    )
    
    # Messages
    MOTIVATIONAL_MESSAGES = [
        os.getenv("MOTIVATIONAL_MESSAGE_1"),
        os.getenv("MOTIVATIONAL_MESSAGE_2")
    ]
    
    TWEETS = [
        os.getenv("TWEET_1"),
        os.getenv("TWEET_2")
    ]
    
    # Admin
    ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
    
    # Validation
    ALLOWED_SPORTS = ["general", "yoga", "running", "weightlifting", "swimming"]
    ALLOWED_GOALS = ["balance", "weight_loss", "muscle_gain", "vegan"]
    
    # Workout Data
    @classmethod
    def get_workout_data(cls) -> dict:
        encoded_data = os.getenv("WORKOUT_DATA")
        if not encoded_data:
            raise ValueError("WORKOUT_DATA environment variable missing")
        return json.loads(base64.b64decode(encoded_data).decode())
    
    # Validation
    @classmethod
    def validate(cls):
        required = ["TELEGRAM_BOT_TOKEN", "DATABASE_URL"]
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required variables: {', '.join(missing)}")