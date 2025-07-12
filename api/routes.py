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
from pydantic import BaseModel
from services.loader import load_inventory, save_inventory, load_action_log
from services.logger import log_post_ai_action
from core.simulator import simulate_day
from core.decision_engine import run_decision_engine
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
from openai import OpenAI
import logging
from difflib import get_close_matches

load_dotenv()
router = APIRouter()

# ===================== INVENTORY =====================
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

# ===================== SIMULATION =====================
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

# ===================== DECISIONS =====================
@router.get("/decisions")
def run_decisions():
    df, summary = run_decision_engine()
    return {"data": df.to_dict(orient="records"), "summary": summary}

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
    log_post_ai_action(
        item_id,
        row["recommended_action"],
        int(row.get("forecasted_waste_units", 0)),
        row["tactical_note"],
        float(row.get("forecasted_waste_value", 0.0)),
    )
    return {
        "status": "success",
        "message": f"Action '{row['recommended_action']}' logged for {row['item_name']}",
        "tactical_note": row["tactical_note"]
    }

# ===================== SUSTAINABILITY =====================
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
    row = item.iloc[0]
    return {
        "co2_kg": round(row["co2_saved_kg"], 2),
        "water_liters": int(row["water_saved_liters"]),
        "meals_saved": round(row["meals_saved"], 2),
        "efficiency_ratio": round(row["efficiency_ratio"], 3),
        "sustainability_score": round(row["sustainability_score"], 2)
    }

# ===================== INSIGHTS & LOGS =====================
@router.get("/inventory/{item_id}/log")
def get_item_log(item_id: str):
    log_df = load_action_log()
    logs = log_df[log_df["item_id"] == item_id].sort_values("timestamp", ascending=False)
    logs = logs.replace([np.inf, -np.inf], np.nan).fillna(0)
    return logs.to_dict(orient="records")

@router.get("/inventory/{item_id}/full")
def get_full_item_view(item_id: str):
    df, _ = run_decision_engine(save=False)
    item = df[df["item_id"] == item_id]
    if item.empty:
        return {"error": "Item not found"}
    row = item.iloc[0].to_dict()
    history = load_action_log()
    logs = history[history["item_id"] == item_id].sort_values("timestamp", ascending=False)
    logs = logs.replace([np.inf, -np.inf], np.nan).fillna(0)
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
        "logs": logs.to_dict(orient="records")
    }

# ===================== AI CHAT ENDPOINT =====================
class ChatRequest(BaseModel):
    item_id: str
    message: str
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def extract_best_match_item(query: str, known_items: list) -> str:
    matches = get_close_matches(query.lower(), [item.lower() for item in known_items], n=1, cutoff=0.6)
    return matches[0] if matches else None

def build_context_for_item(item_id: str) -> str:
    try:
        df, _ = run_decision_engine(save=False)
        item = df[df["item_id"] == item_id]
        if item.empty:
            return "Item not found."
        row = item.iloc[0].to_dict()
        log_df = load_action_log()
        
        logs = log_df[log_df["item_id"] == item_id].sort_values("timestamp", ascending=False).head(5)
        logging.info("📦 Item Preview:\n%s", item.columns) 
        context = f"""Item ID: {row['item_id']}
Item Name: {row['item_name']}
Category: {row['category']}
Description: {row.get('description', 'Fresh quality product')}
Expiry Date: {row.get('expiry_date', 'N/A')}
Quantity: {row['current_stock']}
Recommended Action: {row['recommended_action']} ({row['confidence']}% confidence)
Tactical Note: {row['tactical_note']}
Sustainability:
- CO₂ Saved: {row['co2_saved_kg']}kg
- Water Saved: {row['water_saved_liters']}L
- Meals Saved: {row['meals_saved']}
- Efficiency Ratio: {row['efficiency_ratio']}
- Sustainability Score: {row['sustainability_score']}

Additional Data:
- Department: {row.get('department')}
- Shelf Life (days): {row.get('shelf_life_days')}
- Days Remaining: {row.get('days_remaining')}
- Initial Stock: {row.get('initial_stock')}
- Base Price: {row.get('base_price')}
- Dynamic Price: {row.get('dynamic_price')}
- Daily Sales: {row.get('daily_sales')}
- Elasticity: {row.get('elasticity')}
- Restock Frequency (days): {row.get('restock_frequency_days')}
- Last Restock Date: {row.get('last_restock_date')}
- Next Restock Date: {row.get('next_restock_date')}
- Carbon Score: {row.get('carbon_score')}
- Predicted Monthly Sales: {row.get('predicted_monthly_sales')}
- Predicted Daily Sales: {row.get('predicted_daily_sales')}
- Days Until Restock: {row.get('days_until_restock')}
- Days Stock Lasts: {row.get('days_stock_lasts')}
- Risk Score: {row.get('risk_score')}
- Risk Tag: {row.get('risk_tag')}
- Forecasted Waste Units: {row.get('forecasted_waste_units')}
- Forecasted Waste Value: {row.get('forecasted_waste_value')}
- Energy Saved: {row.get('energy_saved_kwh')}
- Overstock Score: {row.get('overstock_score')}

Recent Actions:"""

        for _, act in logs.iterrows():
            context += f"\n- {act['timestamp']}: {act['action_type']} ({act.get('reason', 'N/A')})"
        return context
    except Exception as e:
        return f"Error: {e}"

def query_llm_with_context(message: str, context: str) -> str:
    logging.info("💬 Message: %s", message)
    logging.info("📦 Context Preview:\n%s", context[:1000]) 
    try:
        prompt = f"""
You are WasteWise AI — a professional assistant for store managers reviewing specific inventory items.
Respond concisely and formally using only the provided context.

📦 ITEM CONTEXT:
{context}

🎯 USER QUERY:
{message}

📋 INSTRUCTIONS:
- Answer the query based only on the context.
- Do not speculate, assume issues, or mention errors.
- Avoid filler, greetings, or unnecessary explanation.
- Use a direct, formal tone suitable for decision-makers.
- If information is not available, reply: "This detail is not available in the item context."
- Keep the response under 50 words.
"""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.exception("LLM failed:")
        return "Unable to process your request at the moment."

@router.post("/chat")
def chat_with_ai(request: ChatRequest):
    try:
        context = build_context_for_item(request.item_id)
        df = load_inventory()
        known_items = df["item_name"].tolist()
        match = extract_best_match_item(request.message, known_items)
        if match:
            current_item = df[df["item_id"] == request.item_id]["item_name"].values[0]
            if match.lower() != current_item.lower():
                context += f"\n\n⚠️ Note: You mentioned '{match}' which may be a different item."
        reply = query_llm_with_context(request.message, context)
        return {"reply": reply, "status": "success"}
    except Exception as e:
        logging.exception("Chat API failed")
        return {"reply": "Something went wrong while processing your request.", "status": "error"}
