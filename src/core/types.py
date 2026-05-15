from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel

class Email(BaseModel):
    sender_name: Optional[str] = None
    sender_email: str
    sender_domain: str
    date: Optional[datetime] = None
    subject: Optional[str] = None
    headers: Dict[str, str] = {}
    body_snippet: Optional[str] = None
    is_spam: bool = False
    is_newsletter: bool = False
    spam_confidence: float = 0.0
    newsletter_confidence: float = 0.0
    spam_reasons: List[str] = []
    newsletter_platform: Optional[str] = None

class AnalyticsResult(BaseModel):
    total_emails: int = 0
    unique_senders: int = 0
    errors: int = 0
    top_senders: List[Dict] = []
    top_domains: List[Dict] = []
    timeline_data: List[Dict] = []
    spam_count: int = 0
    newsletter_count: int = 0
    emails: List[Email] = []
