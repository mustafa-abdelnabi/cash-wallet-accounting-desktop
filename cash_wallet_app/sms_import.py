import re
from datetime import datetime
from typing import Any, Dict, List, Optional


_TRANSACTION_KEYWORDS = {
    "deposit": ["ايداع", "إيداع", "deposit", "cash deposit"],
    "withdrawal": ["سحب", "withdrawal", "cash withdrawal"],
    "incoming_transfer": ["تحويل وارد", "incoming transfer", "transfer in"],
    "outgoing_transfer": ["تحويل صادر", "outgoing transfer", "transfer out"],
}


def _parse_amount(text: str) -> Optional[float]:
    match = re.search(r"(\d+(?:[.,]\d{1,2})?)\s*(?:جنيه|ج.م|EGP|ل٫س|ل.س|جنيهات)?", text)
    if not match:
        return None
    value = match.group(1).replace(",", "")
    try:
        return float(value)
    except ValueError:
        return None


def _parse_date(text: str) -> Optional[str]:
    for pattern in [
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{2}/\d{2}/\d{4})",
        r"(\d{2}-\d{2}-\d{4})",
    ]:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


def parse_sms_message(message: str, wallet_candidates: Optional[List[str]] = None) -> Dict[str, Any]:
    text = (message or "").strip()
    if not text:
        raise ValueError("الرسالة فارغة.")

    amount = _parse_amount(text)
    tx_type = "needs_review"
    for key, phrases in _TRANSACTION_KEYWORDS.items():
        if any(phrase.lower() in text.lower() for phrase in phrases):
            tx_type = key
            break

    wallet_hint = None
    if wallet_candidates:
        normalized = text.lower()
        for candidate in wallet_candidates:
            if candidate.lower() in normalized:
                wallet_hint = candidate
                break

    result = {
        "message": text,
        "amount": amount,
        "transaction_type": tx_type,
        "date": _parse_date(text) or datetime.now().strftime("%Y-%m-%d"),
        "wallet_hint": wallet_hint,
        "customer_reference": None,
        "ambiguous": amount is None or tx_type == "needs_review" or wallet_hint is None,
    }
    return result


def preview_sms_import(message: str, wallet_candidates: Optional[List[str]] = None) -> Dict[str, Any]:
    parsed = parse_sms_message(message, wallet_candidates)
    if parsed["ambiguous"]:
        parsed["status"] = "manual_review_required"
    else:
        parsed["status"] = "ready_for_confirmation"
    return parsed
