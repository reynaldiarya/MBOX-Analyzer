import re
from email.header import decode_header
from email.utils import parseaddr

def decode_str(value: str) -> str:
    """Decode encoded email header (e.g., =?UTF-8?B?...?=)."""
    if not value:
        return ""
    parts = decode_header(value)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try:
                decoded.append(part.decode(charset or "utf-8", errors="replace"))
            except Exception:
                decoded.append(part.decode("latin-1", errors="replace"))
        else:
            decoded.append(part)
    return "".join(decoded).strip()


def parse_sender(from_header: str) -> tuple[str, str]:
    """
    Extract name and email from From header.
    Example: '"John Doe" <john@example.com>' → ('John Doe', 'john@example.com')
    """
    decoded = decode_str(from_header)
    name, email_addr = parseaddr(decoded)
    email_addr = email_addr.lower().strip()

    # Fallback: use regex if parseaddr fails
    if not email_addr or "@" not in email_addr:
        match = re.search(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", decoded)
        email_addr = match.group(0).lower() if match else decoded.lower()
        name = ""

    return name.strip('"').strip(), email_addr
