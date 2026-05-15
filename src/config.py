import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Centralized configuration for the MBOX Analyzer."""
    DEFAULT_TOP_N = int(os.getenv("DEFAULT_TOP_N", 20))
    MAX_TOP_N = int(os.getenv("MAX_TOP_N", 100))
    MIN_TOP_N = int(os.getenv("MIN_TOP_N", 5))
