# config.py - Configuration Management
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Config:
    """Application configuration"""
    
    # App Settings
    APP_NAME = "Finance Pro 2.0"
    APP_VERSION = "2.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "finance_pro_advanced.db")
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_WORKERS = int(os.getenv("API_WORKERS", 4))
    
    # ML/AI Settings
    ML_MODEL_VERSION = "1.0"
    ANOMALY_SENSITIVITY = float(os.getenv("ANOMALY_SENSITIVITY", 0.15))
    PREDICTION_CONFIDENCE_THRESHOLD = float(os.getenv("PREDICTION_CONFIDENCE_THRESHOLD", 0.6))
    
    # Currency Settings
    DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "UGX")
    SUPPORTED_CURRENCIES = ["UGX", "USD", "EUR", "GBP", "KES"]
    
    # Exchange Rate API
    EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY", "")
    EXCHANGE_RATE_API_URL = os.getenv("EXCHANGE_RATE_API_URL", "https://api.exchangerate-api.com/v4/latest")
    
    # Bank Integration Settings
    PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID", "")
    PLAID_SECRET = os.getenv("PLAID_SECRET", "")
    PLAID_ENVIRONMENT = os.getenv("PLAID_ENVIRONMENT", "sandbox")
    
    # User Preferences
    THEME = os.getenv("THEME", "dark")
    LANGUAGE = os.getenv("LANGUAGE", "en")
    DATE_FORMAT = os.getenv("DATE_FORMAT", "%Y-%m-%d")
    TIMEZONE = os.getenv("TIMEZONE", "UTC")
    
    # Kivy UI Settings
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", 400))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", 700))
    
    # Feature Flags
    ENABLE_ML_FEATURES = os.getenv("ENABLE_ML_FEATURES", "True").lower() == "true"
    ENABLE_BANK_SYNC = os.getenv("ENABLE_BANK_SYNC", "False").lower() == "true"
    ENABLE_CLOUD_SYNC = os.getenv("ENABLE_CLOUD_SYNC", "False").lower() == "true"
    ENABLE_ANALYTICS = os.getenv("ENABLE_ANALYTICS", "True").lower() == "true"
    
    # Notification Settings
    ENABLE_BUDGET_ALERTS = os.getenv("ENABLE_BUDGET_ALERTS", "True").lower() == "true"
    ENABLE_ANOMALY_ALERTS = os.getenv("ENABLE_ANOMALY_ALERTS", "True").lower() == "true"
    BUDGET_ALERT_THRESHOLD = int(os.getenv("BUDGET_ALERT_THRESHOLD", 80))
    
    # Backup & Export
    BACKUP_ENABLED = os.getenv("BACKUP_ENABLED", "True").lower() == "true"
    BACKUP_FREQUENCY = os.getenv("BACKUP_FREQUENCY", "daily")  # daily, weekly, monthly
    BACKUP_PATH = os.getenv("BACKUP_PATH", "./backups")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "finance_pro.log")
    
    # Categories (Customizable)
    DEFAULT_CATEGORIES = [
        "Groceries", "Utilities", "Transport", "Entertainment",
        "Dining", "Healthcare", "Education", "Shopping",
        "Rent", "Savings", "Other"
    ]
    
    # Payment Methods
    PAYMENT_METHODS = [
        "Cash", "Debit Card", "Credit Card", "Bank Transfer",
        "Mobile Money", "Wallet", "Check"
    ]
    
    @classmethod
    def get_env(cls, key: str, default: Optional[str] = None) -> str:
        """Get environment variable with fallback"""
        return os.getenv(key, default)
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production"""
        return not cls.DEBUG
    
    @classmethod
    def get_config_dict(cls) -> dict:
        """Get configuration as dictionary"""
        return {
            'app': {
                'name': cls.APP_NAME,
                'version': cls.APP_VERSION,
                'debug': cls.DEBUG,
            },
            'database': {
                'path': cls.DB_PATH,
                'url': cls.DATABASE_URL,
            },
            'api': {
                'host': cls.API_HOST,
                'port': cls.API_PORT,
            },
            'ml': {
                'enabled': cls.ENABLE_ML_FEATURES,
                'anomaly_sensitivity': cls.ANOMALY_SENSITIVITY,
            },
            'currency': {
                'default': cls.DEFAULT_CURRENCY,
                'supported': cls.SUPPORTED_CURRENCIES,
            }
        }
