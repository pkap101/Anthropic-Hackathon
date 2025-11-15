"""
Application configuration settings for the Grader UI
"""
import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    """Configuration for the Gradio UI application"""
    
    # Backend API settings (where your FastAPI grader is running)
    API_PROTOCOL = os.getenv("API_PROTOCOL", "http")
    API_HOST = os.getenv("API_HOST", "localhost")  # Change to your backend host
    API_PORT = int(os.getenv("API_PORT", "8000"))  # Your FastAPI port
    
    # Gradio UI settings (where this UI will run)
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")  # 0.0.0.0 allows external access
    APP_PORT = int(os.getenv("APP_PORT", "7860"))  # Gradio default port

CONFIG = AppConfig()