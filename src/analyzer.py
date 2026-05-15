import mailbox
import os
from collections import Counter
from src.config import Settings
from src.parser import parse_sender

DEFAULT_TOP_N = Settings.DEFAULT_TOP_N

def analyze_mbox(mbox_path: str, top_n: int = DEFAULT_TOP_N) -> dict:
    """
    Analyze MBOX file and return sender statistics.
    Args:
        mbox_path: Path to .mbox file
        top_n: Number of top senders to return
    Returns:
        dict: {
            "total": int,
            "errors": int,
            "sender_counter": Counter,
            "sender_names": dict,
            "top_senders": list of (email, count) tuples
        }
    """
    if not os.path.exists(mbox_path):
        raise FileNotFoundError(f"File not found: {mbox_path}")

    mbox = mailbox.mbox(mbox_path)

    sender_counter: Counter = Counter()
    sender_names: dict[str, str] = {}  # email → latest name
    total = 0
    errors = 0

    for message in mbox:
        try:
            from_header = message.get("From", "")
            if not from_header:
                continue

            name, email_addr = parse_sender(from_header)
            if not email_addr:
                continue

            sender_counter[email_addr] += 1
            if name and email_addr not in sender_names:
                sender_names[email_addr] = name

            total += 1

        except Exception:
            errors += 1

    top_senders = sender_counter.most_common(top_n)

    return {
        "total": total,
        "errors": errors,
        "sender_counter": sender_counter,
        "sender_names": sender_names,
        "top_senders": top_senders,
        "top_n": top_n
    }
