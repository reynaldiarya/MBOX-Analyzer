import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEFAULT_TOP_N: int = int(os.getenv("DEFAULT_TOP_N", 20))
    MAX_TOP_N: int = int(os.getenv("MAX_TOP_N", 100))
    MIN_TOP_N: int = int(os.getenv("MIN_TOP_N", 5))
