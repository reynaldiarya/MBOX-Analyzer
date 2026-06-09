from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
from typing import Tuple, Optional
from .types import Email


def decode_str(value: str) -> str:
    if not value:
        return ""
    decoded_parts = []
    for part, charset in decode_header(value):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(charset or "utf-8", errors="ignore"))
        else:
            decoded_parts.append(part)
    return "".join(decoded_parts).strip()


def parse_sender(from_header: str) -> Tuple[Optional[str], str, str]:
    name, email = parseaddr(from_header)
    name = decode_str(name) if name else None
    email = email.strip().lower()
    domain = email.split("@")[-1] if "@" in email else ""
    return (name, email, domain)


def parse_email(msg) -> Email:
    # Parse sender
    from_header = msg.get("From", "")
    name, email, domain = parse_sender(from_header)

    # Parse date
    date = None
    date_header = msg.get("Date")
    if date_header:
        try:
            date = parsedate_to_datetime(date_header)
        except Exception:
            pass

    # Parse subject
    subject_header = msg.get("Subject", "")
    subject = decode_str(subject_header) if subject_header else None

    # Parse headers
    headers = dict(msg.items())

    # Body snippet
    body_snippet = None
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    body = payload.decode(charset, errors="ignore") if payload else ""
                    body_snippet = body[:200].strip()
                    break
                except Exception:
                    pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset() or "utf-8"
            body = payload.decode(charset, errors="ignore") if payload else ""
            body_snippet = body[:200].strip()
        except Exception:
            pass

    return Email(
        sender_name=name,
        sender_email=email,
        sender_domain=domain,
        date=date,
        subject=subject,
        headers=headers,
        body_snippet=body_snippet,
    )
