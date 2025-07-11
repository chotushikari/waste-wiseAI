# # agents/genai_agent.py

# import os
# import pandas as pd
# from langchain.chat_models import ChatGroq
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from agents.prompts import *
# from services.loader import load_inventory
# from core.waste_intelligence import enrich_inventory
# from core.sustainability import enrich_sustainability

# # Setup LLM from Groq
# llm = ChatGroq(temperature=0.2, model_name="mixtral-8x7b-32768", api_key=os.getenv("GROQ_API_KEY"))

# # Load and enrich inventory
# _df = enrich_sustainability(enrich_inventory(load_inventory()))

# ### === Daily Overview ===

# def get_daily_summary(mode="balanced"):
#     top_risk = _df.sort_values("risk_score", ascending=False).head(10)
#     prompt = PromptTemplate.from_template(daily_summary_prompt)
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run(items=top_risk.to_dict(orient="records"), mode=mode)

# ### === Item-Level Actions ===

# def ask_about_item(item_name: str, mode="balanced"):
#     item = _df[_df["item_name"].str.lower() == item_name.lower()].head(1)
#     if item.empty:
#         return f"❌ Item '{item_name}' not found in inventory."
#     row = item.iloc[0].to_dict()
#     prompt = PromptTemplate.from_template(item_risk_prompt)
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run(**row, mode=mode)

# def explain_risk_of_item(item_name: str):
#     item = _df[_df["item_name"].str.lower() == item_name.lower()].head(1)
#     if item.empty:
#         return f"❌ No data for {item_name}."
#     row = item.iloc[0].to_dict()
#     prompt = PromptTemplate.from_template(item_risk_prompt)
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run(**row)

# ### === Sustainability Optimizer ===

# def optimize_today_for_sustainability():
#     impact_df = _df[_df["forecasted_waste_units"] > 0]
#     impact_df = impact_df.sort_values("co2_saved_kg", ascending=False).head(20)
#     prompt = PromptTemplate.from_template(sustainability_optimizer_prompt)
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run(items=impact_df.to_dict(orient="records"))

# ### === ROI-Based Return Recommender ===

# def recommend_returns():
#     roi_df = _df[_df["forecasted_waste_value"] > 100]
#     roi_df = roi_df.sort_values("forecasted_waste_value", ascending=False).head(10)
#     prompt = PromptTemplate.from_template(return_value_prompt)
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run(items=roi_df.to_dict(orient="records"))

# ### === Category & Department Insights ===

# def summarize_category(category: str, mode="balanced"):
#     subset = _df[_df["category"].str.lower() == category.lower()]
#     if subset.empty:
#         return f"❌ No items found in category '{category}'."
#     prompt = PromptTemplate.from_template(category_summary_prompt)
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run(category=category, items=subset.to_dict(orient="records"), mode=mode)

# def summarize_department(department: str, mode="balanced"):
#     subset = _df[_df["department"].str.lower() == department.lower()]
#     if subset.empty:
#         return f"❌ No items found in department '{department}'."
#     prompt = PromptTemplate.from_template(department_summary_prompt)
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run(department=department, items=subset.to_dict(orient="records"), mode=mode)

# def full_inventory_summary(mode="balanced"):
#     prompt = PromptTemplate.from_template(full_inventory_overview_prompt)
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run(items=_df.to_dict(orient="records"), mode=mode)

# if __name__ == "__main__":
#     print("\n📊 Daily Summary:")
#     print(get_daily_summary())

#     print("\n🔍 Ask About Item: Milk")
#     print(ask_about_item("Milk"))

#     print("\n🧠 Why is 'Banana' High Risk?")
#     print(explain_risk_of_item("Banana"))

#     print("\n♻️ Optimize for Sustainability:")
#     print(optimize_today_for_sustainability())

#     print("\n📦 Recommend Returns:")
#     print(recommend_returns())

#     print("\n📚 Category Summary: Dairy")
#     print(summarize_category("Dairy"))

#     print("\n🏬 Department Summary: Grocery")
#     print(summarize_department("Grocery"))

#     print("\n📦 Full Inventory Overview:")
#     print(full_inventory_summary())
# agents/genai_agent.py

# agents/genai_agent.py

# agents/genai_agent.py

import os
import pandas as pd
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from agents.prompts import *
from services.loader import load_inventory
from core.waste_intelligence import enrich_inventory
from core.sustainability import enrich_sustainability
from services.feedback import log_feedback
from dotenv import load_dotenv
load_dotenv()

# Load and enrich inventory
_df = enrich_sustainability(enrich_inventory(load_inventory()))

# Setup LLM from Groq
llm = ChatGroq(
    temperature=0.2,
    model_name="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

# Setup memory for conversational context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

### === DAILY SUMMARY OF FULL INVENTORY ===
def get_daily_summary():
    prompt = PromptTemplate.from_template(daily_summary_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(items=_df.to_dict(orient="records"))

### === ITEM-LEVEL SMART LOOKUP ===
def ask_about_item(item_name: str):
    item = _df[_df["item_name"].str.lower().str.contains(item_name.lower())]
    if item.empty:
        return f"❌ Item '{item_name}' not found in inventory."
    row = item.iloc[0].to_dict()
    prompt = PromptTemplate.from_template(item_risk_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(**row)

def explain_risk_of_item(item_name: str):
    item = _df[_df["item_name"].str.lower().str.contains(item_name.lower())]
    if item.empty:
        return f"❌ No data for {item_name}."
    row = item.iloc[0].to_dict()
    prompt = PromptTemplate.from_template(item_risk_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(**row)

def suggest_follow_ups(item_name: str):
    item = _df[_df["item_name"].str.lower().str.contains(item_name.lower())]
    if item.empty:
        return f"⚠️ No match for '{item_name}' in inventory."
    row = item.iloc[0].to_dict()
    prompt = PromptTemplate.from_template(followup_suggestions_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(**row)

### === CATEGORY & DEPARTMENT INSIGHTS ===
def category_summary(category: str):
    category_df = _df[_df["category"].str.lower() == category.lower()]
    if category_df.empty:
        return f"❌ No items in category '{category}'."
    prompt = PromptTemplate.from_template(category_summary_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(category=category, items=category_df.to_dict(orient="records"))

def department_summary(department: str):
    dept_df = _df[_df["department"].str.lower() == department.lower()]
    if dept_df.empty:
        return f"❌ No items in department '{department}'."
    prompt = PromptTemplate.from_template(department_summary_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(department=department, items=dept_df.to_dict(orient="records"))

### === SUSTAINABILITY OPTIMIZER ===
def optimize_today_for_sustainability():
    impact_df = _df[_df["forecasted_waste_units"] > 0]
    impact_df = impact_df.sort_values("co2_saved_kg", ascending=False)
    prompt = PromptTemplate.from_template(sustainability_optimizer_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(items=impact_df.to_dict(orient="records"))

### === ROI-BASED RETURN RECOMMENDER ===
def recommend_returns():
    roi_df = _df[_df["forecasted_waste_value"] > 100]
    roi_df = roi_df.sort_values("forecasted_waste_value", ascending=False)
    prompt = PromptTemplate.from_template(return_value_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(items=roi_df.to_dict(orient="records"))

### === FULL INTELLIGENCE DECISION DIVE ===
def get_full_action_plan():
    prompt = PromptTemplate.from_template(full_decision_plan_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(items=_df.to_dict(orient="records"))

### === SMART QUERY ROUTING (GENERIC CHAT INTERFACE) ===
def smart_inventory_response(query: str):
    prompt = PromptTemplate.from_template(query_router_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain.run(inventory=_df.to_dict(orient="records"), question=query)

def log_user_feedback(user_id, item_id, query, ai_response, rating, comment=""):
    log_feedback(user_id, item_id, query, ai_response, rating, comment)
    return "✅ Feedback recorded. Thank you!"


if __name__ == "__main__":
    print("\n📊 Daily Summary:")
    print(get_daily_summary())

    print("\n🔍 Ask About Item: Milk")
    print(ask_about_item("Milk"))

    print("\n🧠 Why is 'Banana' High Risk?")
    print(explain_risk_of_item("Banana"))

    print("\n💡 Follow-up Suggestions for 'Milk'")
    print(suggest_follow_ups("Milk"))

    print("\n♻️ Optimize for Sustainability:")
    print(optimize_today_for_sustainability())

    print("\n📦 Recommend Returns:")
    print(recommend_returns())

    print("\n🧠 Full Inventory Action Plan:")
    print(get_full_action_plan())

    print("\n💬 Smart Query: 'Which items should be donated today?'")
    print(smart_inventory_response("Which items should be donated today?"))