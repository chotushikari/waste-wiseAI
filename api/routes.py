# # api/routes.py

# from fastapi import APIRouter, Request
# from services.loader import load_inventory, save_inventory
# from core.simulator import simulate_day
# from core.decision_engine import run_decision_engine
# # from agents.genai_agent import (
# #     smart_inventory_response,
# #     ask_about_item,
# #     explain_risk_of_item,
# #     suggest_follow_ups,
# #     get_daily_summary,
# #     optimize_today_for_sustainability,
# #     recommend_returns,
# #     get_full_action_plan,
# # )
# import pandas as pd

# router = APIRouter()

# # Internal loader
# _df = load_inventory()

# # === INVENTORY & SIMULATION ROUTES ===
# @router.get("/inventory")
# def get_inventory():
#     return load_inventory().to_dict(orient="records")

# @router.post("/simulate")
# def simulate():
#     df = simulate_day()
#     return {"status": "success", "message": "1 day simulated", "inventory": df.to_dict(orient="records")}

# @router.post("/simulate/reset")
# def reset_inventory():
#     # Reset logic placeholder: Could re-copy a template inventory file
#     return {"status": "pending", "message": "Reset logic not yet implemented"}

# @router.get("/inventory/item/{item_name}")
# def get_item_data(item_name: str):
#     df = load_inventory()
#     item = df[df["item_name"].str.lower().str.contains(item_name.lower())]
#     if item.empty:
#         return {"error": f"Item '{item_name}' not found"}
#     return item.to_dict(orient="records")


# # === DECISION & INSIGHT ROUTES ===
# @router.get("/decisions")
# def run_decisions():
#     df, summary = run_decision_engine()
#     return {"data": df.to_dict(orient="records"), "summary": summary}

# @router.get("/decisions/summary")
# def get_summary():
#     _, summary = run_decision_engine(save=False)
#     return summary

# @router.get("/decisions/{item_name}")
# def get_decision_note(item_name: str):
#     df, _ = run_decision_engine(save=False)
#     item = df[df["item_name"].str.lower().str.contains(item_name.lower())]
#     if item.empty:
#         return {"note": "Item not found"}
#     return {"note": item.iloc[0].get("tactical_note", "No note available")}

# @router.get("/returns/recommend")
# def recommend_return():
#     return recommend_returns()


# # === SUSTAINABILITY ROUTES ===
# @router.get("/sustainability/impact")
# def get_sustainability():
#     df, _ = run_decision_engine(save=False)
#     return {
#         "co2_kg": round(df["co2_saved_kg"].sum(), 2),
#         "meals": int(df["meals_saved"].sum()),
#         "water_liters": int(df["water_saved_liters"].sum())
#     }

# @router.get("/sustainability/optimizer")
# def get_sustainability_plan():
#     return optimize_today_for_sustainability()


# # === GENAI AGENT / CHATBOT ROUTES ===
# @router.get("/ask")
# def query_inventory(q: str):
#     return smart_inventory_response(q)

# @router.get("/item/{item_name}/explain")
# def explain_item_risk(item_name: str):
#     return explain_risk_of_item(item_name)

# @router.get("/item/{item_name}/followups")
# def suggest_item_followups(item_name: str):
#     return suggest_follow_ups(item_name)

# @router.get("/summary/daily")
# def genai_daily_summary():
#     return get_daily_summary()

# @router.get("/action/plan")
# def genai_full_plan():
#     return get_full_action_plan()


# # === MISC / UTIL ===
# @router.get("/health")
# def health_check():
#     return {"status": "up", "message": "Wastewise AI backend is alive!"}

# # api/routes.py

# from fastapi import APIRouter
# from services.loader import load_inventory, save_inventory, load_action_log
# from services.logger import log_post_ai_action
# from core.simulator import simulate_day
# from core.decision_engine import run_decision_engine
# import pandas as pd

# router = APIRouter()


# # === INVENTORY ===
# @router.get("/inventory")
# def get_inventory():
#     return load_inventory().to_dict(orient="records")

# @router.get("/inventory/itemid/{item_id}")
# def get_item_by_id(item_id: str):
#     df = load_inventory()
#     item = df[df["item_id"] == item_id]
#     if item.empty:
#         return {"error": "Item not found"}
#     return item.to_dict(orient="records")[0]

# @router.get("/inventory/item/{item_name}")
# def get_item_by_name(item_name: str):
#     df = load_inventory()
#     item = df[df["item_name"].str.lower().str.contains(item_name.lower())]
#     if item.empty:
#         return {"error": f"Item '{item_name}' not found"}
#     return item.to_dict(orient="records")


# # === SIMULATION ===
# @router.post("/simulate")
# def simulate():
#     df, summary = simulate_day()
#     return {
#         "status": "success",
#         "message": "1 day simulated",
#         "summary": summary,
#         "inventory": df.to_dict(orient="records")
#     }

# @router.post("/simulate/reset")
# def reset_inventory():
#     # You can replace this with a logic to copy from a backup inventory template
#     return {"status": "pending", "message": "Reset logic not yet implemented"}


# # === AI DECISIONS ===
# @router.get("/decisions")
# def run_decisions():
#     df, summary = run_decision_engine()
#     return {
#         "data": df.to_dict(orient="records"),
#         "summary": summary
#     }

# @router.get("/decisions/summary")
# def get_summary():
#     _, summary = run_decision_engine(save=False)
#     return summary

# @router.get("/inventory/{item_id}/decision")
# def get_decision_for_item(item_id: str):
#     df, _ = run_decision_engine(save=False)
#     item = df[df["item_id"] == item_id]
#     if item.empty:
#         return {"error": "Item not found"}
#     return {
#         "action": item.iloc[0]["recommended_action"],
#         "note": item.iloc[0]["tactical_note"],
#         "confidence": item.iloc[0]["confidence"]
#     }

# @router.post("/inventory/{item_id}/action")
# def apply_ai_action(item_id: str):
#     df, _ = run_decision_engine(save=False)
#     item = df[df["item_id"] == item_id]
#     if item.empty:
#         return {"error": "Item not found"}

#     row = item.iloc[0]
#     log_post_ai_action(row)
#     return {
#         "status": "success",
#         "message": f"Action '{row['recommended_action']}' logged for {row['item_name']}",
#         "tactical_note": row["tactical_note"]
#     }


# # === SUSTAINABILITY ===
# @router.get("/sustainability/impact")
# def get_total_sustainability():
#     df, _ = run_decision_engine(save=False)
#     return {
#         "co2_kg": round(df["co2_saved_kg"].sum(), 2),
#         "meals": int(df["meals_saved"].sum()),
#         "water_liters": int(df["water_saved_liters"].sum())
#     }

# @router.get("/inventory/{item_id}/impact")
# def get_sustainability_for_item(item_id: str):
#     df, _ = run_decision_engine(save=False)
#     item = df[df["item_id"] == item_id]
#     if item.empty:
#         return {"error": "Item not found"}
#     return {
#         "co2_kg": round(item.iloc[0]["co2_saved_kg"], 2),
#         "water_liters": int(item.iloc[0]["water_saved_liters"]),
#         "meals_saved": round(item.iloc[0]["meals_saved"], 2),
#         "efficiency_ratio": round(item.iloc[0]["efficiency_ratio"], 3),
#         "sustainability_score": round(item.iloc[0]["sustainability_score"], 2),
#     }


# # === LOGS & HISTORY ===
# @router.get("/inventory/{item_id}/log")
# def get_item_log(item_id: str):
#     log_df = load_action_log()
#     item_logs = log_df[log_df["item_id"] == item_id].sort_values("timestamp", ascending=False)
#     return item_logs.to_dict(orient="records")


# # === FULL FRONTEND ITEM VIEW ===
# @router.get("/inventory/{item_id}/full")
# def get_full_item_view(item_id: str):
#     df, _ = run_decision_engine(save=False)
#     item = df[df["item_id"] == item_id]
#     if item.empty:
#         return {"error": "Item not found"}

#     row = item.iloc[0].to_dict()

#     history = load_action_log()
#     item_logs = history[history["item_id"] == item_id]

#     if "timestamp" in item_logs.columns and not item_logs.empty:
#         item_logs = item_logs.sort_values("timestamp", ascending=False)

#     return {
#         "item": row,
#         "decision": {
#             "action": row["recommended_action"],
#             "note": row["tactical_note"],
#             "confidence": row["confidence"]
#         },
#         "sustainability": {
#             "co2_kg": row["co2_saved_kg"],
#             "meals_saved": row["meals_saved"],
#             "water_liters": row["water_saved_liters"]
#         },
#         "logs": item_logs.to_dict(orient="records")
#     }


# # === MISC ===
# @router.get("/health")
# def health_check():
#     return {"status": "up", "message": "Wastewise AI backend is alive!"}

from fastapi import APIRouter
from services.loader import load_inventory, save_inventory, load_action_log
from services.logger import log_post_ai_action
from core.simulator import simulate_day
from core.decision_engine import run_decision_engine
import pandas as pd

router = APIRouter()

# === INVENTORY ===
@router.get("/inventory")
def get_inventory():
    return load_inventory().to_dict(orient="records")

@router.get("/inventory/itemid/{item_id}")
def get_item_by_id(item_id: str):
    df = load_inventory()
    item = df[df["item_id"] == item_id]
    if item.empty:
        return {"error": "Item not found"}
    return item.to_dict(orient="records")[0]

@router.get("/inventory/item/{item_name}")
def get_item_by_name(item_name: str):
    df = load_inventory()
    item = df[df["item_name"].str.lower().str.contains(item_name.lower())]
    if item.empty:
        return {"error": f"Item '{item_name}' not found"}
    return item.to_dict(orient="records")

# === SIMULATION ===
@router.post("/simulate")
def simulate():
    df, summary = simulate_day()
    return {
        "status": "success",
        "message": "1 day simulated",
        "summary": summary,
        "inventory": df.to_dict(orient="records")
    }

@router.post("/simulate/reset")
def reset_inventory():
    return {"status": "pending", "message": "Reset logic not yet implemented"}

# === AI DECISIONS ===
@router.get("/decisions")
def run_decisions():
    df, summary = run_decision_engine()
    return {
        "data": df.to_dict(orient="records"),
        "summary": summary
    }

@router.get("/decisions/summary")
def get_summary():
    _, summary = run_decision_engine(save=False)
    return summary

@router.get("/inventory/{item_id}/decision")
def get_decision_for_item(item_id: str):
    df, _ = run_decision_engine(save=False)
    item = df[df["item_id"] == item_id]
    if item.empty:
        return {"error": "Item not found"}
    return {
        "action": item.iloc[0]["recommended_action"],
        "note": item.iloc[0]["tactical_note"],
        "confidence": item.iloc[0]["confidence"]
    }

@router.post("/inventory/{item_id}/action")
def apply_ai_action(item_id: str):
    df, _ = run_decision_engine(save=False)
    item = df[df["item_id"] == item_id]
    if item.empty:
        return {"error": "Item not found"}

    row = item.iloc[0]

    # Extract required values
    action = row["recommended_action"]
    quantity = int(row.get("forecasted_waste_units", 0))
    reason = row["tactical_note"]
    value = float(row.get("forecasted_waste_value", 0.0))

    # ✅ Call the logger with explicit arguments
    log_post_ai_action(item_id, action, quantity, reason, value)

    return {
        "status": "success",
        "message": f"Action '{action}' logged for {row['item_name']}",
        "tactical_note": reason
    }


# === SUSTAINABILITY ===
@router.get("/sustainability/impact")
def get_total_sustainability():
    df, _ = run_decision_engine(save=False)
    return {
        "co2_kg": round(df["co2_saved_kg"].sum(), 2),
        "meals": int(df["meals_saved"].sum()),
        "water_liters": int(df["water_saved_liters"].sum())
    }

@router.get("/inventory/{item_id}/impact")
def get_sustainability_for_item(item_id: str):
    df, _ = run_decision_engine(save=False)
    item = df[df["item_id"] == item_id]
    if item.empty:
        return {"error": "Item not found"}
    return {
        "co2_kg": round(item.iloc[0]["co2_saved_kg"], 2),
        "water_liters": int(item.iloc[0]["water_saved_liters"]),
        "meals_saved": round(item.iloc[0]["meals_saved"], 2),
        "efficiency_ratio": round(item.iloc[0]["efficiency_ratio"], 3),
        "sustainability_score": round(item.iloc[0]["sustainability_score"], 2),
    }

# === INSIGHTS & LEADERBOARD ===
@router.get("/insights/waste-trend")
def get_daily_waste_trend():
    df = load_action_log()
    if "timestamp" not in df.columns:
        return {"error": "No logs found"}
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    spoilage = df[df["action_type"] == "spoilage"].groupby("date").agg({
        "quantity": "sum",
        "value": "sum"
    }).reset_index()
    return spoilage.to_dict(orient="records")

@router.get("/insights/category")
def get_category_sustainability_impact():
    df, _ = run_decision_engine(save=False)
    agg = df.groupby("category").agg({
        "co2_saved_kg": "sum",
        "meals_saved": "sum",
        "water_saved_liters": "sum"
    }).sort_values("co2_saved_kg", ascending=False).reset_index()
    return agg.to_dict(orient="records")

@router.get("/leaderboard")
def get_top_sustainable_items():
    df, _ = run_decision_engine(save=False)
    top_items = df.sort_values("sustainability_score", ascending=False).head(10)
    return top_items[["item_id", "item_name", "sustainability_score", "co2_saved_kg", "meals_saved"]].to_dict(orient="records")

# === LOGS & HISTORY ===
import numpy as np

@router.get("/inventory/{item_id}/log")
def get_item_log(item_id: str):
    log_df = load_action_log()
    item_logs = log_df[log_df["item_id"] == item_id].sort_values("timestamp", ascending=False)
    
    # Replace problematic float values
    item_logs = item_logs.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return item_logs.to_dict(orient="records")

# === FULL ITEM VIEW ===
@router.get("/inventory/{item_id}/full")
def get_full_item_view(item_id: str):
    df, _ = run_decision_engine(save=False)
    item = df[df["item_id"] == item_id]
    if item.empty:
        return {"error": "Item not found"}
    row = item.iloc[0].to_dict()
    history = load_action_log()
    item_logs = history[history["item_id"] == item_id]
    if "timestamp" in item_logs.columns and not item_logs.empty:
        item_logs = item_logs.sort_values("timestamp", ascending=False)

    # Replace problematic float values
    item_logs = item_logs.replace([np.inf, -np.inf], np.nan).fillna(0)

    return {
        "item": row,
        "decision": {
            "action": row["recommended_action"],
            "note": row["tactical_note"],
            "confidence": row["confidence"]
        },
        "sustainability": {
            "co2_kg": row["co2_saved_kg"],
            "meals_saved": row["meals_saved"],
            "water_liters": row["water_saved_liters"]
        },
        "logs": item_logs.to_dict(orient="records")
    }

# === MISC ===
@router.get("/health")
def health_check():
    return {"status": "up", "message": "Wastewise AI backend is alive!"}
