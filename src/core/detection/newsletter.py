from typing import Dict

def detect_newsletter(email_obj) -> Dict:
    is_newsletter = False
    confidence = 0.0
    platform = None
    reasons = []

    # Check X-Mailer header
    x_mailer = email_obj.headers.get("X-Mailer", "").lower()
    platforms = {
        "mailchimp": "Mailchimp",
        "substack": "Substack",
        "beehiiv": "Beehiiv",
        "convertkit": "ConvertKit",
        "sendgrid": "SendGrid"
    }
    for key, name in platforms.items():
        if key in x_mailer:
            is_newsletter = True
            confidence += 0.4
            platform = name
            reasons.append(f"Detected {name} via X-Mailer header")
            break

    # Check sender domain
    if not platform:
        sender_domain = email_obj.sender_domain.lower()
        domain_platforms = {
            "mailchimp.com": "Mailchimp",
            "substack.com": "Substack",
            "beehiiv.com": "Beehiiv",
            "convertkit.com": "ConvertKit",
            "sendgrid.net": "SendGrid"
        }
        for domain, name in domain_platforms.items():
            if domain in sender_domain:
                is_newsletter = True
                confidence += 0.3
                platform = name
                reasons.append(f"Detected {name} via sender domain")
                break

    # List-Unsubscribe header
    if "List-Unsubscribe" in email_obj.headers:
        is_newsletter = True
        confidence += 0.3
        reasons.append("Contains List-Unsubscribe header")

    # Newsletter keywords
    newsletter_keywords = ["newsletter", "weekly update", "daily digest", "bulletin"]
    subject_lower = (email_obj.subject or "").lower()
    for kw in newsletter_keywords:
        if kw in subject_lower:
            is_newsletter = True
            confidence += 0.2
            reasons.append(f"Contains newsletter keyword: {kw}")
            break

    confidence = min(confidence, 1.0)
    if confidence > 0.5:
        is_newsletter = True

    return {
        "is_newsletter": is_newsletter,
        "confidence": confidence,
        "platform": platform,
        "reasons": reasons
    }
