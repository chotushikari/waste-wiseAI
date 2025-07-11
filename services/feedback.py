# services/feedback.py
import pandas as pd
from datetime import datetime

def log_feedback(user_id, item_id, query, ai_response, rating, comment=""):
    df = pd.DataFrame([{
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "item_id": item_id,
        "query": query,
        "ai_response": ai_response,
        "rating": rating,  # 1–5 stars
        "comment": comment
    }])
    
    try:
        existing = pd.read_csv("data/feedback_log.csv")
        df = pd.concat([existing, df], ignore_index=True)
    except FileNotFoundError:
        pass
    
    df.to_csv("data/feedback_log.csv", index=False)
