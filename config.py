"""
Configuration settings for Play Store Trend Analyzer
"""
import os

class Config:
    """Configuration settings"""
    
    # App settings
    APP_ID = "in.swiggy.android"
    COUNTRY = "in"
    LANGUAGE = "en"
    
    # Processing settings
    LOOKBACK_DAYS = 30
    MAX_REVIEWS_PER_DAY = 50
    MIN_TOPIC_FREQUENCY = 2
    
    # Topic settings
    SEED_TOPICS = [
        "Delivery issue",
        "Food stale",
        "Delivery partner rude",
        "App crashing",
        "Payment issue",
        "Order cancellation",
        "Refund problem",
        "Food quality poor",
        "Wrong order delivered",
        "Long delivery time",
        "Customer support unresponsive",
        "Order tracking not accurate",
        "Food packaging damaged",
        "Missing items in order",
        "Coupon not working",
        "App login problem",
        "Too many notifications",
        "Delivery charges high",
        "Restaurant not available"
    ]
    
    # Output settings
    OUTPUT_DIR = "./output"
    REPORTS_DIR = "./output/reports"
    
    @staticmethod
    def ensure_directories():
        """Create necessary directories"""
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
        os.makedirs("./data", exist_ok=True)