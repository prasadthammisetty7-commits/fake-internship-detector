# fake_internship_detector_rule_based.py
import re

SUSPICIOUS_KEYWORDS = [
    "registration fee", "processing fee", "security deposit", "pay to apply",
    "upfront payment", "send money", "bitcoin", "crypto", "usdt", "gift card",
    "telegram only", "whatsapp only", "dm for details", "no interview", "instant selection",
    "limited slots", "act fast", "guaranteed certificate", "guaranteed job", "earn ₹",
    "work from home no skills", "no experience required high salary"
]

SUSPICIOUS_PATTERNS = [
    r"\b(pay|payment)\b.*\b(before|prior)\b",            # pay before selection
    r"\bcontact\b.*\b(telegram|whatsapp)\b",             # off-platform contact
    r"\b(no interview|no test|no screening)\b",          # no formal process
    r"\b(stipend)\b.*\b(after\b.*\bfee\b)",              # stipend tied to fees
    r"\b(certificate)\b.*\b(guarantee|assured)\b",       # guaranteed certificate
]

UNREALISTIC_PHRASES = [
    "₹1,00,000 per month for intern", "high salary no experience", "instant stipend",
    "earn daily ₹5000", "salary in crypto only"
]

RISK_FACTORS = {
    "fee_mentions": 3,
    "crypto_only": 3,
    "off_platform": 2,
    "no_process": 2,
    "guarantees": 2,
    "unrealistic": 3,
    "unknown_email_domain": 2,
    "personal_email_contact": 2
}

TRUSTED_EMAIL_DOMAINS = [
    "google.com", "microsoft.com", "amazon.com", "meta.com", "ibm.com"
]

def extract_emails(text):
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

def domain_from_email(email):
    return email.split("@")[-1].lower()

def score_text(text: str) -> dict:
    t = text.lower()
    score = 0
    reasons = []

    # keyword hits
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in t:
            score += 2
            reasons.append(f"Keyword: '{kw}'")

    # regex patterns
    for pat in SUSPICIOUS_PATTERNS:
        if re.search(pat, t):
            score += 2
            reasons.append(f"Pattern matched: {pat}")

    # unrealistic claims
    for phrase in UNREALISTIC_PHRASES:
        if phrase in t:
            score += RISK_FACTORS["unrealistic"]
            reasons.append(f"Unrealistic: '{phrase}'")

    # payments in crypto only
    if "crypto only" in t or ("bitcoin" in t and "only" in t):
        score += RISK_FACTORS["crypto_only"]
        reasons.append("Crypto-only payment")

    # off-platform contact
    if "telegram" in t or "whatsapp" in t or "dm" in t:
        score += RISK_FACTORS["off_platform"]
        reasons.append("Off-platform contact")

    # guarantees
    if "guaranteed" in t or "assured" in t:
        score += RISK_FACTORS["guarantees"]
        reasons.append("Guarantee language")

    # no process claims
    if "no interview" in t or "instant selection" in t:
        score += RISK_FACTORS["no_process"]
        reasons.append("No interview/instant selection")

    # email domain checks
    emails = extract_emails(text)
    if emails:
        for e in emails:
            dom = domain_from_email(e)
            # personal email providers
            if any(dom.endswith(p) for p in ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "proton.me", "rediffmail.com"]):
                score += RISK_FACTORS["personal_email_contact"]
                reasons.append(f"Personal email: {e}")
            # unknown corporate domain (not in trusted list)
            elif dom not in TRUSTED_EMAIL_DOMAINS and not re.search(r"\b(intern|careers|jobs)\b", text.lower()):
                score += RISK_FACTORS["unknown_email_domain"]
                reasons.append(f"Unverified domain: {dom}")

    risk_level = "Low"
    if score >= 10:
        risk_level = "High"
    elif score >= 6:
        risk_level = "Medium"

    return {"risk_score": score, "risk_level": risk_level, "reasons": reasons}

def predict(text: str) -> dict:
    result = score_text(text)
    result["label"] = "Fake" if result["risk_level"] in ["High", "Medium"] else "Likely Genuine"
    return result

if __name__ == "__main__":
    print("FAKE INTERNSHIP DETECTOR")
    print("------------------------")

    sample = input("Paste internship message: ")

    res = predict(sample)

    print("\nResult")
    print("------")
    print("Risk score:", res["risk_score"])
    print("Risk level:", res["risk_level"])
    print("Label:", res["label"])

    print("\nReasons:")
    for r in res["reasons"]:
        print("-", r)
    sample = input("paste internship message:")
    res = predict(sample)
    print("Risk score:", res["risk_score"])
    print("Risk level:", res["risk_level"])
    print("Label:", res["label"])
    print("Reasons:")
    for r in res["reasons"]:
        print("-", r)