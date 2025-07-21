import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Healthcare MCP Server with OpenRouter"""
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-4")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1500"))
    
    # Vector DB Configuration
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./healthcare_db")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # Streamlit Configuration
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    
    # Healthcare-specific Configuration
    HEALTHCARE_COLLECTION = os.getenv("HEALTHCARE_COLLECTION", "healthcare_knowledge")
    MEDICAL_DISCLAIMER = os.getenv("MEDICAL_DISCLAIMER", 
        "This AI assistant provides general health information only and should not replace professional medical advice, diagnosis, or treatment.")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is required. Please set it in your .env file.")
        
        return True 