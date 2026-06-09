from collections import Counter
import mailbox
from datetime import datetime
from typing import List, Optional, Tuple
from .parser import parse_email
from .config import Settings
from .types import Email, AnalyticsResult
from .detection.spam import detect_spam
from .detection.newsletter import detect_newsletter


def analyze_mbox(
    mbox_path: str,
    top_n: int = 10,
    date_range: Optional[Tuple[datetime, datetime]] = None,
    sender_filter: Optional[List[str]] = None,
    domain_filter: Optional[List[str]] = None,
) -> AnalyticsResult:
    sender_counter = Counter()
    domain_counter = Counter()
    sender_names = {}
    errors = 0
    total = 0
    emails: List[Email] = []
    timeline = Counter()

    settings = Settings()
    top_n = max(settings.MIN_TOP_N, min(top_n, settings.MAX_TOP_N))

    try:
        mbox = mailbox.mbox(mbox_path)
        for msg in mbox:
            try:
                email_obj = parse_email(msg)

                # Apply filters
                if date_range and email_obj.date:
                    start, end = date_range
                    if not (start <= email_obj.date <= end):
                        continue
                if sender_filter and email_obj.sender_email not in sender_filter:
                    continue
                if domain_filter and email_obj.sender_domain not in domain_filter:
                    continue

                # Detect spam and newsletter
                spam_result = detect_spam(email_obj)
                email_obj.is_spam = spam_result["is_spam"]
                email_obj.spam_confidence = spam_result["confidence"]
                email_obj.spam_reasons = spam_result["reasons"]

                newsletter_result = detect_newsletter(email_obj)
                email_obj.is_newsletter = newsletter_result["is_newsletter"]
                email_obj.newsletter_confidence = newsletter_result["confidence"]
                email_obj.newsletter_platform = newsletter_result["platform"]

                emails.append(email_obj)
                total += 1

                # Update counters
                if email_obj.sender_email:
                    sender_counter[email_obj.sender_email] += 1
                    if email_obj.sender_email not in sender_names:
                        sender_names[email_obj.sender_email] = email_obj.sender_name
                if email_obj.sender_domain:
                    domain_counter[email_obj.sender_domain] += 1
                if email_obj.date:
                    day_key = email_obj.date.strftime("%Y-%m-%d")
                    timeline[day_key] += 1

            except Exception:
                errors += 1

        # Top senders
        top_senders = sender_counter.most_common(top_n)
        top_senders_list = [
            {
                "rank": i + 1,
                "email": email,
                "name": sender_names.get(email, ""),
                "count": count,
                "percentage": (count / total) * 100 if total > 0 else 0.0,
            }
            for i, (email, count) in enumerate(top_senders)
        ]

        # Top domains
        top_domains = domain_counter.most_common(top_n)
        top_domains_list = [
            {
                "rank": i + 1,
                "domain": domain,
                "count": count,
                "percentage": (count / total) * 100 if total > 0 else 0.0,
            }
            for i, (domain, count) in enumerate(top_domains)
        ]

        # Timeline data
        timeline_sorted = sorted(timeline.items(), key=lambda x: x[0])
        timeline_data = [
            {"date": date, "count": count} for date, count in timeline_sorted
        ]

        spam_count = sum(1 for e in emails if e.is_spam)
        newsletter_count = sum(1 for e in emails if e.is_newsletter)

        return AnalyticsResult(
            total_emails=total,
            unique_senders=len(sender_counter),
            errors=errors,
            top_senders=top_senders_list,
            top_domains=top_domains_list,
            timeline_data=timeline_data,
            spam_count=spam_count,
            newsletter_count=newsletter_count,
            emails=emails,
        )

    except Exception:
        return AnalyticsResult(errors=1)
