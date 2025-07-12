# # services/logger.py

# import csv
# from datetime import datetime
# from services.config import LOG_FILE

# # Global queue for batched logs
# ACTION_LOG_QUEUE = []

# def log_action(item_id, action_type, quantity, reason="", value=0.0):
#     ACTION_LOG_QUEUE.append({
#         "timestamp": datetime.now().isoformat(),
#         "item_id": item_id,
#         "action_type": action_type,
#         "quantity": quantity,
#         "reason": reason,
#         "value": round(value, 2)
#     })

# def flush_logs_to_file():
#     if not ACTION_LOG_QUEUE:
#         return
    
#     try:
#         with open(LOG_FILE, "a", newline="") as file:
#             fieldnames = ["timestamp", "item_id", "action_type", "quantity", "reason", "value"]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             if file.tell() == 0:
#                 writer.writeheader()
#             writer.writerows(ACTION_LOG_QUEUE)
#     except Exception as e:
#         print(f"[❌ Logger Error] Failed to write batch log: {e}")
#     finally:
#         ACTION_LOG_QUEUE.clear()

# services/logger.py

# import csv
# from datetime import datetime
# from services.config import LOG_FILE

# # Global queue for batched logs
# ACTION_LOG_QUEUE = []

# def log_action(item_id, action_type, quantity, reason="", value=0.0):
#     """
#     Log a single action. Adds to the queue.
#     """
#     ACTION_LOG_QUEUE.append({
#         "timestamp": datetime.now().isoformat(),
#         "item_id": item_id,
#         "action_type": action_type,
#         "quantity": quantity,
#         "reason": reason,
#         "value": round(value, 2)
#     })

# def batch_log_action(entries: list[dict]):
#     """
#     Add multiple log entries to the queue.
#     """
#     timestamp = datetime.now().isoformat()
#     for entry in entries:
#         ACTION_LOG_QUEUE.append({
#             "timestamp": timestamp,
#             "item_id": entry.get("item_id"),
#             "action_type": entry.get("action_type"),
#             "quantity": entry.get("quantity"),
#             "reason": entry.get("reason", ""),
#             "value": round(entry.get("value", 0.0), 2)
#         })

# def flush_logs_to_file():
#     """
#     Write all queued logs to CSV in one go.
#     """
#     if not ACTION_LOG_QUEUE:
#         return

#     try:
#         with open(LOG_FILE, "a", newline="") as file:
#             fieldnames = ["timestamp", "item_id", "action_type", "quantity", "reason", "value"]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             if file.tell() == 0:
#                 writer.writeheader()
#             writer.writerows(ACTION_LOG_QUEUE)
#     except Exception as e:
#         print(f"[❌ Logger Error] Failed to write batch log: {e}")
#     finally:
#         ACTION_LOG_QUEUE.clear()

# import csv
# from datetime import datetime
# from services.config import ACTION_LOG_CSV

# # Global queue for batched logs
# ACTION_LOG_QUEUE = []

# def log_action(item_id, action_type, quantity, reason="", value=0.0):
#     """
#     Log a single action. Adds to the queue.
#     """
#     ACTION_LOG_QUEUE.append({
#         "timestamp": datetime.now().isoformat(),
#         "item_id": item_id,
#         "action_type": action_type,
#         "quantity": quantity,
#         "reason": reason,
#         "value": round(value, 2)
#     })

# def batch_log_action(entries: list[dict]):
#     """
#     Add multiple log entries to the queue.
#     """
#     timestamp = datetime.now().isoformat()
#     for entry in entries:
#         ACTION_LOG_QUEUE.append({
#             "timestamp": timestamp,
#             "item_id": entry.get("item_id"),
#             "action_type": entry.get("action_type"),
#             "quantity": entry.get("quantity"),
#             "reason": entry.get("reason", ""),
#             "value": round(entry.get("value", 0.0), 2)
#         })

# def flush_logs_to_file():
#     """
#     Write all queued logs to CSV in one go.
#     """
#     if not ACTION_LOG_QUEUE:
#         return

#     try:
#         with open(ACTION_LOG_CSV, mode="a", newline="", encoding="utf-8") as file:
#             fieldnames = ["timestamp", "item_id", "action_type", "quantity", "reason", "value"]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)

#             # Write header if the file is empty
#             if file.tell() == 0:
#                 writer.writeheader()

#             writer.writerows(ACTION_LOG_QUEUE)

#     except Exception as e:
#         print(f"[❌ Logger Error] Failed to write batch log: {e}")
#     finally:
#         ACTION_LOG_QUEUE.clear()

# # === Smart Logging Utilities ===
# def log_if_changed(current_df, prev_snapshot):
#     logs = []
#     for _, row in current_df.iterrows():
#         prev = prev_snapshot.get(row['item_id'], {})
#         changed = False
        
#         if prev.get('action') != row['recommended_action']:
#             changed = True
#             reason = "AI Action Changed"
#         elif prev.get('dynamic_price') != row['dynamic_price']:
#             changed = True
#             reason = "Price Updated"
#         elif prev.get('risk_tag') != row['risk_tag']:
#             changed = True
#             reason = "Risk Status Changed"
#         else:
#             continue  # No significant change

#         logs.append({
#             'item_id': row['item_id'],
#             'action_type': row['recommended_action'],
#             'quantity': row['forecasted_waste_units'],
#             'reason': reason,
#             'value': round(row['forecasted_waste_value'], 2)
#         })

#     return logs

# def take_snapshot(df):
#     return {
#         row['item_id']: {
#             'action': row['recommended_action'],
#             'dynamic_price': row['dynamic_price'],
#             'risk_tag': row['risk_tag']
#         }
#         for _, row in df.iterrows()
#     }


import os
import csv
from datetime import datetime
import pandas as pd
from services.config import ACTION_LOG_CSV, ACTION_LOG_PARQUET

# In-memory batch queue
ACTION_LOG_QUEUE = []

# Central action filter (import from config if defined there)
IMPORTANT_ACTIONS = {
    "spoilage", "sale", "restock",
    "DONATE", "RETURN to Supplier",
    "Strategic Discount - Tier 1", "Strategic Discount - Tier 2"
}

# === BASIC ACTION LOGGING ===

def log_action(item_id, action_type, quantity, reason="", value=0.0):
    """Log a single action if important."""
    if action_type not in IMPORTANT_ACTIONS:
        return
    ACTION_LOG_QUEUE.append({
        "timestamp": datetime.now().isoformat(),
        "item_id": str(item_id),
        "action_type": action_type,
        "quantity": int(quantity),
        "reason": reason,
        "value": round(float(value), 2)
    })


def batch_log_action(entries: list[dict]):
    """Log multiple actions at once, filter unimportant."""
    timestamp = datetime.now().isoformat()
    for entry in entries:
        if entry.get("action_type") not in IMPORTANT_ACTIONS:
            continue
        ACTION_LOG_QUEUE.append({
            "timestamp": timestamp,
            "item_id": str(entry.get("item_id")),
            "action_type": entry.get("action_type"),
            "quantity": int(entry.get("quantity", 0)),
            "reason": entry.get("reason", ""),
            "value": round(float(entry.get("value", 0.0)), 2)
        })


def flush_logs_to_file():
    """Flush queued actions to CSV log file."""
    if not ACTION_LOG_QUEUE:
        return

    try:
        with open(ACTION_LOG_CSV, "a", newline="", encoding="utf-8") as file:
            fieldnames = ["timestamp", "item_id", "action_type", "quantity", "reason", "value"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(ACTION_LOG_QUEUE)
    except Exception as e:
        print(f"[❌ Logger Error] Failed to write log batch: {e}")
    finally:
        ACTION_LOG_QUEUE.clear()


# === FULL AI CONTEXT LOGGING FOR ML TRAINING ===

def log_full_action_context(df, date=None):
    """Logs full AI decision context for actions worth saving (CSV + Parquet)."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    loggable = df[df['recommended_action'].isin(IMPORTANT_ACTIONS)].copy()
    if loggable.empty:
        return

    try:
        # Select relevant columns
        log_df = loggable[[
            "item_id", "current_stock", "days_remaining", "base_price", "dynamic_price",
            "forecasted_waste_units", "forecasted_waste_value", "predicted_daily_sales",
            "co2_saved_kg", "sustainability_score", "efficiency_ratio",
            "recommended_action", "tactical_note", "risk_tag", "category", "department"
        ]].copy()

        # Derived fields
        log_df["timestamp"] = datetime.now().isoformat()
        log_df["action_type"] = log_df["recommended_action"]
        log_df["quantity"] = log_df["forecasted_waste_units"]
        log_df["reason"] = log_df["tactical_note"]
        log_df["value"] = log_df["forecasted_waste_value"]
        log_df["date"] = date

        # Final order
        ordered_cols = [
            "timestamp", "item_id", "action_type", "quantity", "reason", "value",
            "current_stock", "days_remaining", "base_price", "dynamic_price",
            "forecasted_waste_units", "forecasted_waste_value", "predicted_daily_sales",
            "co2_saved_kg", "sustainability_score", "efficiency_ratio",
            "risk_tag", "date", "category", "department"
        ]
        log_df = log_df[ordered_cols]

        # Safe typecasting
        numeric_cols = log_df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            log_df[col] = pd.to_numeric(log_df[col], errors="coerce").fillna(0)

        # Load existing log if available
        if os.path.exists(ACTION_LOG_CSV):
            existing_df = pd.read_csv(ACTION_LOG_CSV, dtype=str)
            combined_df = pd.concat([existing_df, log_df.astype(str)], ignore_index=True)
        else:
            combined_df = log_df.astype(str)

        # Save both formats
        combined_df.to_csv(ACTION_LOG_CSV, index=False)
        combined_df.to_parquet(ACTION_LOG_PARQUET, index=False)

        print(f"✅ Logged {len(log_df)} full-context AI actions to CSV and Parquet")

    except Exception as e:
        print(f"[❌ Full Log Error] Failed to log AI actions: {e}")

def log_post_ai_action(item_id, action, quantity, reason, value):
    log_entry = {
        "item_id": item_id,
        "action_type": action,
        "quantity": quantity,
        "reason": reason,
        "value": round(value, 2)
    }
    batch_log_action([log_entry])
    flush_logs_to_file() 