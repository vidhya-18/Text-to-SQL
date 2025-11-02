import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    """
    Loads configuration variables from the environment.
    """
    # --- Groq API Configuration (FIXED) ---
    GROQ_API_KEY = os.getenv("GROQ_API")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "gemma2-9b-it")
    
    # --- Database Configuration ---
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    
    @property
    def database_url(self) -> str:
        """
        Generates the full database connection URL.
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"