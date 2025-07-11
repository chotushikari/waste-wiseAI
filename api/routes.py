# api/routes.py

from fastapi import APIRouter, Request
from services.loader import load_inventory, save_inventory
from core.simulator import simulate_day
from core.decision_engine import run_decision_engine
from agents.genai_agent import (
    smart_inventory_response,
    ask_about_item,
    explain_risk_of_item,
    suggest_follow_ups,
    get_daily_summary,
    optimize_today_for_sustainability,
    recommend_returns,
    get_full_action_plan,
)
import pandas as pd

router = APIRouter()

# Internal loader
_df = load_inventory()

# === INVENTORY & SIMULATION ROUTES ===
@router.get("/inventory")
def get_inventory():
    return load_inventory().to_dict(orient="records")

@router.post("/simulate")
def simulate():
    df = simulate_day()
    return {"status": "success", "message": "1 day simulated", "inventory": df.to_dict(orient="records")}

@router.post("/simulate/reset")
def reset_inventory():
    # Reset logic placeholder: Could re-copy a template inventory file
    return {"status": "pending", "message": "Reset logic not yet implemented"}

@router.get("/inventory/item/{item_name}")
def get_item_data(item_name: str):
    df = load_inventory()
    item = df[df["item_name"].str.lower().str.contains(item_name.lower())]
    if item.empty:
        return {"error": f"Item '{item_name}' not found"}
    return item.to_dict(orient="records")


# === DECISION & INSIGHT ROUTES ===
@router.get("/decisions")
def run_decisions():
    df, summary = run_decision_engine()
    return {"data": df.to_dict(orient="records"), "summary": summary}

@router.get("/decisions/summary")
def get_summary():
    _, summary = run_decision_engine(save=False)
    return summary

@router.get("/decisions/{item_name}")
def get_decision_note(item_name: str):
    df, _ = run_decision_engine(save=False)
    item = df[df["item_name"].str.lower().str.contains(item_name.lower())]
    if item.empty:
        return {"note": "Item not found"}
    return {"note": item.iloc[0].get("tactical_note", "No note available")}

@router.get("/returns/recommend")
def recommend_return():
    return recommend_returns()


# === SUSTAINABILITY ROUTES ===
@router.get("/sustainability/impact")
def get_sustainability():
    df, _ = run_decision_engine(save=False)
    return {
        "co2_kg": round(df["co2_saved_kg"].sum(), 2),
        "meals": int(df["meals_saved"].sum()),
        "water_liters": int(df["water_saved_liters"].sum())
    }

@router.get("/sustainability/optimizer")
def get_sustainability_plan():
    return optimize_today_for_sustainability()


# === GENAI AGENT / CHATBOT ROUTES ===
@router.get("/ask")
def query_inventory(q: str):
    return smart_inventory_response(q)

@router.get("/item/{item_name}/explain")
def explain_item_risk(item_name: str):
    return explain_risk_of_item(item_name)

@router.get("/item/{item_name}/followups")
def suggest_item_followups(item_name: str):
    return suggest_follow_ups(item_name)

@router.get("/summary/daily")
def genai_daily_summary():
    return get_daily_summary()

@router.get("/action/plan")
def genai_full_plan():
    return get_full_action_plan()


# === MISC / UTIL ===
@router.get("/health")
def health_check():
    return {"status": "up", "message": "Wastewise AI backend is alive!"}
