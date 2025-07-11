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


import csv
import os
from datetime import datetime
import pandas as pd
from services.config import ACTION_LOG_CSV, ACTION_LOG_PARQUET

# In-memory action queue
ACTION_LOG_QUEUE = []

# Only log important events (skip low-value NO ACTION etc.)
IMPORTANT_ACTIONS = {"spoilage", "sale", "restock", "DONATE", "RETURN to Supplier", "MARKDOWN -10%", "MARKDOWN -30%"}


# === BASIC ACTION LOGGING ===
def log_action(item_id, action_type, quantity, reason="", value=0.0):
    if action_type not in IMPORTANT_ACTIONS:
        return
    ACTION_LOG_QUEUE.append({
        "timestamp": datetime.now().isoformat(),
        "item_id": item_id,
        "action_type": action_type,
        "quantity": quantity,
        "reason": reason,
        "value": round(value, 2)
    })

def batch_log_action(entries: list[dict]):
    timestamp = datetime.now().isoformat()
    for entry in entries:
        if entry.get("action_type") not in IMPORTANT_ACTIONS:
            continue
        ACTION_LOG_QUEUE.append({
            "timestamp": timestamp,
            "item_id": entry.get("item_id"),
            "action_type": entry.get("action_type"),
            "quantity": entry.get("quantity", 0),
            "reason": entry.get("reason", ""),
            "value": round(entry.get("value", 0.0), 2)
        })

def flush_logs_to_file():
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
        print(f"[❌ Logger Error] Failed to write batch log: {e}")
    finally:
        ACTION_LOG_QUEUE.clear()


# === PARQUET FORMAT (Full AI Decision Logs for ML Training) ===
def log_full_action_context(df, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Filter for important actions
    loggable = df[df['recommended_action'].isin(["DONATE", "RETURN to Supplier", "MARKDOWN -10%", "MARKDOWN -30%"])]

    if loggable.empty:
        return

    try:
        # Select and copy the relevant columns
        log_df = loggable[[
            "item_id", "department", "current_stock", "days_remaining", "base_price", "dynamic_price",
            "forecasted_waste_units", "forecasted_waste_value", "predicted_daily_sales",
            "co2_saved_kg", "sustainability_score", "efficiency_ratio",
            "recommended_action", "tactical_note", "risk_tag"
        ]].copy()

        # Add the date column
        log_df["date"] = date

        # Append to existing logs if the Parquet file exists
        if os.path.exists(ACTION_LOG_PARQUET):
            existing = pd.read_parquet(ACTION_LOG_PARQUET)
            log_df = pd.concat([existing, log_df], ignore_index=True)

        # Save to Parquet
        log_df.to_parquet(ACTION_LOG_PARQUET, index=False)

        # Save to CSV
        log_df.to_csv(ACTION_LOG_CSV, index=False)

        print(f"✅ Logged {len(log_df)} full-context AI actions to Parquet and CSV")

    except Exception as e:
        print(f"[❌ Full Log Error] Failed to write AI log: {e}")

def log_post_ai_action(row):
    log_action(
        item_id=row["item_id"],
        action_type=row["recommended_action"],
        quantity=row["forecasted_waste_units"],
        reason=row["tactical_note"],
        value=row["forecasted_waste_value"]
    )
