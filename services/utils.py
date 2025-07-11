# services/utils.py

from datetime import datetime
import re

def clean_item_name(name: str) -> str:
    """
    Normalize item name (lowercase, remove punctuation).
    """
    name = name.lower().strip()
    return re.sub(r"[^\w\s]", "", name)

def get_current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_currency(value: float) -> str:
    return f"₹{round(value, 2):,.2f}"

def percentage(part: float, whole: float) -> float:
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)

def is_high_risk(score: float) -> bool:
    return score >= 75

def is_medium_risk(score: float) -> bool:
    return 45 <= score < 75

def is_low_risk(score: float) -> bool:
    return score < 45

def truncate_string(text: str, max_chars: int = 80) -> str:
    return text if len(text) <= max_chars else text[:max_chars] + "..."

def capitalize_words(text: str) -> str:
    return " ".join(word.capitalize() for word in text.split())
