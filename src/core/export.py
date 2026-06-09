import csv
import io
from typing import List, Dict
from .types import AnalyticsResult


def generate_csv_content(result: AnalyticsResult) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    output.write("\ufeff")  # BOM for Excel
    writer.writerow(
        [
            "Date",
            "Sender Email",
            "Sender Name",
            "Domain",
            "Subject",
            "Is Spam",
            "Spam Confidence",
            "Spam Reasons",
            "Is Newsletter",
            "Newsletter Confidence",
            "Newsletter Platform",
        ]
    )
    for email in result.emails:
        date_str = email.date.strftime("%Y-%m-%d %H:%M:%S") if email.date else ""
        spam_reasons_str = "; ".join(email.spam_reasons) if email.spam_reasons else ""
        writer.writerow(
            [
                date_str,
                email.sender_email,
                email.sender_name or "",
                email.sender_domain,
                email.subject or "",
                "Yes" if email.is_spam else "No",
                f"{email.spam_confidence:.2f}",
                spam_reasons_str,
                "Yes" if email.is_newsletter else "No",
                f"{email.newsletter_confidence:.2f}",
                email.newsletter_platform or "",
            ]
        )
    return output.getvalue()


def generate_top_senders_csv(top_senders: List[Dict]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    output.write("\ufeff")
    writer.writerow(["Rank", "Email", "Name", "Count", "% of Total"])
    for sender in top_senders:
        writer.writerow(
            [
                sender["rank"],
                sender["email"],
                sender["name"],
                sender["count"],
                f"{sender['percentage']:.2f}%",
            ]
        )
    return output.getvalue()
