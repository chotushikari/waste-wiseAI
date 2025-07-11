# # agents/assistant_chatbot.py

# import streamlit as st
# import os
# from langchain.chat_models import ChatGroq
# from langchain.chains import ConversationChain
# from langchain.prompts import PromptTemplate
# from agents.memory import get_conversation_memory
# from services.loader import load_inventory
# from core.waste_intelligence import enrich_inventory
# from core.sustainability import enrich_sustainability

# # === Load and enrich full inventory context ===
# df = enrich_sustainability(enrich_inventory(load_inventory()))
# inventory_records = df.to_dict(orient="records")

# # === Setup LLM ===
# llm = ChatGroq(
#     temperature=0.2,
#     model_name="mixtral-8x7b-32768",
#     api_key=os.getenv("GROQ_API_KEY")
# )

# # === System Prompt ===
# system_prompt = PromptTemplate.from_template("""
# You are WasteWise AI — an executive-grade inventory expert.
# You help store managers and sustainability leads:
# - Reduce spoilage and losses
# - Optimize CO₂, water, and meal impact
# - Take smart actions like markdowns, donations, returns
# - Give fast insights and explain actions clearly

# 🧠 You support advanced features:
# - 🔍 Smart item lookup
# - 🎯 Suggested follow-up
# - 🧠 Session memory
# - 🔁 Context recall
# - 📈 Action recommendations

# 🛒 Inventory Today:
# {inventory}

# Now respond to the query:
# User: {input}
# """)

# # === Setup memory ===
# memory = get_conversation_memory()

# # === Chat Chain ===
# chat_chain = ConversationChain(
#     llm=llm,
#     memory=memory,
#     prompt=system_prompt
# )

# # === Streamlit UI ===
# def run_assistant():
#     st.set_page_config(page_title="WasteWise AI Assistant", page_icon="🧠")
#     st.title("🧠 WasteWise Inventory Assistant")
#     st.caption("Ask about stock risk, CO₂ impact, restocks, markdowns & more.")

#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     user_input = st.chat_input("E.g. 'Risk for Milk today' or 'Optimize my returns'")

#     if user_input:
#         with st.spinner("Thinking like a sustainability strategist..."):
#             response = chat_chain.run(input=user_input, inventory=inventory_records)
#             st.session_state.chat_history.append((user_input, response))

#     # Display chat history
#     for user, bot in reversed(st.session_state.chat_history):
#         st.chat_message("user").markdown(f"**You:** {user}")
#         st.chat_message("ai").markdown(f"{bot}")

# if __name__ == "__main__":
#     run_assistant()


import re
from difflib import get_close_matches
from agents.genai_agent import (
    ask_about_item,
    explain_risk_of_item,
    suggest_follow_ups,
    smart_inventory_response,
    get_daily_summary,
    optimize_today_for_sustainability,
    recommend_returns,
    get_full_action_plan,
)
from services.loader import load_inventory

# === Load live item names ===
def get_all_item_names():
    df = load_inventory()
    return df["item_name"].dropna().unique().tolist()

# === Fuzzy Smart Item Matcher ===
def extract_best_match_item(query: str, known_items: list[str]) -> str | None:
    query = query.lower()
    matches = get_close_matches(query, [item.lower() for item in known_items], n=1, cutoff=0.6)
    if matches:
        matched_lower = matches[0]
        for item in known_items:
            if item.lower() == matched_lower:
                return item
    return None

# === Suggested FAQs ===
def generate_faq_followups(item_name: str):
    return suggest_follow_ups(item_name)

# === MAIN QUERY DISPATCHER ===
def handle_inventory_query(query: str):
    known_items = get_all_item_names()
    item_name = extract_best_match_item(query, known_items)

    query_lower = query.lower()

    # Info Request
    if any(kw in query_lower for kw in ["what is", "tell me about", "details", "info"]):
        if item_name:
            return ask_about_item(item_name)

    # Risk Inquiry
    if any(kw in query_lower for kw in ["risk", "why flagged", "high risk"]):
        if item_name:
            return explain_risk_of_item(item_name)

    # Follow-up Suggestions
    if any(kw in query_lower for kw in ["follow-up", "next", "more about"]):
        if item_name:
            return generate_faq_followups(item_name)

    # Daily Status
    if any(kw in query_lower for kw in ["summary", "status", "overview", "today"]):
        return get_daily_summary()

    # Sustainability
    if "sustainability" in query_lower or "carbon" in query_lower:
        return optimize_today_for_sustainability()

    # Return Suggestions
    if "return" in query_lower or "supplier" in query_lower:
        return recommend_returns()

    # Full Action Plan
    if "action plan" in query_lower or "full analysis" in query_lower:
        return get_full_action_plan()

    # Fallback: Smart Response
    return smart_inventory_response(query)
