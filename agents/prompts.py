# agents/prompts.py

# === DAILY FULL INVENTORY SUMMARY ===
daily_summary_prompt = """
You're a Walmart-grade retail inventory intelligence analyst.

Today’s full inventory status is provided below. Your job is to give a **daily executive summary** for the operations and sustainability lead, including:

1. ⚠️ SKUs with highest waste risk (mention a few key ones).
2. 🛠️ Recommended actions (return, markdown, donation) with brief justifications.
3. 📉 Top contributors to potential financial loss.
4. 🌍 Sustainability red flags (items with high CO₂ or water waste).
5. 📊 Overall health of stock: overstock, fast-moving, and stagnant categories.
6. 💡 Bonus: Creative ideas to prevent waste or improve turnover.

Inventory Snapshot:
{items}

Keep it concise but actionable. Use bullet points and emojis for clarity. Write like a consultant speaking to leadership.
"""

# === ITEM RISK EXPLANATION ===
item_risk_prompt = """
You're a retail GenAI expert advisor.

Explain why the following item is currently flagged as high/medium/low risk:

Item Details:
{item_name}
Current Stock: {current_stock}
Shelf Life: {shelf_life_days} days
Days Remaining: {days_remaining}
Dynamic Price: ₹{dynamic_price}
Base Price: ₹{base_price}
Elasticity: {elasticity}
Forecasted Waste: ₹{forecasted_waste_value}
Carbon Score: {carbon_score}
Risk Score: {risk_score}
Recommended Action: {recommended_action}
Risk Tag: {risk_tag}

Provide a clear explanation of the risk, contributing factors, and a data-backed rationale for the recommendation.
"""

# === CATEGORY SUMMARY ===
category_summary_prompt = """
You're assisting a retail operations planner.

Give a smart, category-level summary for **{category}** items. Analyze inventory performance and recommend immediate actions.

Inputs:
- High-risk items (based on score)
- Inventory levels and sales velocity
- Spoilage risk and restock cycles
- Sustainability impact

Goals:
- Reduce waste and CO₂ footprint
- Recommend actionable interventions (e.g., markdown %, donation, return)
- Identify best/worst performers
- Detect unusual patterns or opportunities

Category Snapshot:
{items}

Respond in executive tone with short insights + next-step actions.
"""

# === DEPARTMENT SUMMARY ===
department_summary_prompt = """
You are a supply chain strategist for a retail department.

Based on today's data for department **{department}**, summarize:

- 🔍 SKU-level hotspots (name a few)
- 🟢 Stable items
- 🔴 Urgent items needing action
- ♻️ Sustainability issues (e.g., carbon, water)
- 💰 Where we’re losing the most value

Data:
{items}

Provide 3–5 clear recommendations tailored to department-level decisions.
"""

# === SUSTAINABILITY OPTIMIZER ===
sustainability_optimizer_prompt = """
You are a sustainability optimization AI.

Based on this inventory, design a plan to maximize environmental savings:

- Reduce CO₂ impact and water waste
- Avoid spoilage through markdown or donation
- Suggest operational changes or awareness strategies

Data:
{items}

List top 3–5 changes or focus areas with their estimated impact.
"""

# === ITEM-LEVEL ACTIONS ===
return_value_prompt = """
You are a returns strategist.

From the following items, choose those best suited for return to supplier. Justify based on:

- Predicted spoilage value
- Shelf life remaining
- Demand elasticity
- ROI from return vs. markdown vs. donation

Data:
{items}

Present 3–5 actionable returns with reasoning.
"""

# === FULL INVENTORY STRATEGIC PLAN ===
full_decision_plan_prompt = """
Act as a Chief Inventory Strategist.

Perform a full inventory audit and provide:

1. 🔎 Strategic Overview: What’s the current situation?
2. 🧩 Top 5 Priorities Today (across departments)
3. 🔁 Suggested Global Actions (bulk restocks, markdown campaigns, donations)
4. 📦 Highlight Categories Most at Risk
5. ♻️ Sustainability Alert Zones (High CO₂ or Water Waste)

Here’s the data:
{items}

Keep output structured. Use bullet points and label sections clearly. Include brief data points or item names when relevant.
"""

# === SMART QUERY ROUTER ===
query_router_prompt = """
Act as a smart AI assistant for Walmart inventory.

Given a user query and today's inventory data, respond intelligently:
- Route to specific item info if item is mentioned
- Generate list if asking about risk, donation, spoilage, returns
- Provide a short, confident response with deep insight
- Suggest 1 follow-up question at end

Inventory: {inventory}
Query: {question}
"""

# === FOLLOW-UP SUGGESTIONS ===
followup_suggestions_prompt = """
Suggest 3 intelligent follow-up questions about the item "{item_name}" that a Walmart associate might ask.

Examples:
- Action-related ("Should I markdown this?")
- Sustainability-focused ("How much CO₂ can I save?")
- Risk analysis ("Why is risk so high?")

Respond only with 3 bullets.
"""
