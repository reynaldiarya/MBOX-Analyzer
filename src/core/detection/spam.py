import re
from typing import Dict

def detect_spam(email_obj) -> Dict:
    is_spam = False
    confidence = 0.0
    reasons = []

    # 1. Detect noreply@
    if email_obj.sender_email.startswith("noreply@") or "noreply" in email_obj.sender_email:
        is_spam = True
        confidence += 0.3
        reasons.append("Sender is noreply address")

    # 2. Marketing keywords
    marketing_keywords = ["sale", "discount", "offer", "promo", "marketing", "advertisement", "buy now", "limited time"]
    subject_lower = (email_obj.subject or "").lower()
    body_lower = (email_obj.body_snippet or "").lower()
    for kw in marketing_keywords:
        if kw in subject_lower or kw in body_lower:
            is_spam = True
            confidence += 0.2
            reasons.append(f"Contains marketing keyword: {kw}")
            break

    # 3. Bulk email headers
    bulk_headers = ["X-Bulk-Mail", "X-Mass-Mail", "X-Bulk", "X-Mailing-List"]
    for header in bulk_headers:
        if header in email_obj.headers:
            is_spam = True
            confidence += 0.3
            reasons.append(f"Contains bulk email header: {header}")

    # 4. Unsubscribe headers
    if "List-Unsubscribe" in email_obj.headers:
        is_spam = True
        confidence += 0.2
        reasons.append("Contains List-Unsubscribe header")

    # 5. Suspicious sender patterns
    if '@' in email_obj.sender_email:
        local_part = email_obj.sender_email.split('@')[0]
        if re.search(r'[0-9]{5,}', local_part) or re.search(r'[a-z]{20,}', local_part):
            is_spam = True
            confidence += 0.2
            reasons.append("Suspicious sender local part pattern")

    confidence = min(confidence, 1.0)
    if confidence > 0.5:
        is_spam = True

    return {
        "is_spam": is_spam,
        "confidence": confidence,
        "reasons": reasons
    }
