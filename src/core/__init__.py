from .types import Email, AnalyticsResult
from .parser import parse_email, parse_sender, decode_str
from .analyzer import analyze_mbox
from .config import Settings
from .export import generate_csv_content
from .detection.spam import detect_spam
from .detection.newsletter import detect_newsletter

__all__ = [
    "Email", "AnalyticsResult",
    "parse_email", "parse_sender", "decode_str",
    "analyze_mbox", "Settings", "generate_csv_content",
    "detect_spam", "detect_newsletter"
]
