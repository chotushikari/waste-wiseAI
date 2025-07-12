# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import numpy as np
# from datetime import datetime, timedelta
# import sys
# import os
# # Add project root to path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from services.loader import load_inventory, load_action_log
# from core.decision_engine import run_decision_engine
# from agents.genai_agent import (
#     get_daily_summary, 
#     optimize_today_for_sustainability,
#     recommend_returns,
#     get_full_action_plan
# )

# # Page configuration
# st.set_page_config(
#     page_title="WasteWise AI Dashboard",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .metric-card {
#         background-color: #f0f2f6;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         border-left: 4px solid #1f77b4;
#     }
#     .high-risk {
#         border-left-color: #d62728;
#     }
#     .medium-risk {
#         border-left-color: #ff7f0e;
#     }
#     .low-risk {
#         border-left-color: #2ca02c;
#     }
# </style>
# """, unsafe_allow_html=True)

# @st.cache_data(ttl=300)  # Cache for 5 minutes
# def load_data():
#     """Load and cache inventory data"""
#     try:
#         df = load_inventory()
#         return df
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return pd.DataFrame()

# @st.cache_data(ttl=300)
# def load_logs():
#     """Load and cache action logs"""
#     try:
#         logs = load_action_log()
#         if not logs.empty:
#             logs['timestamp'] = pd.to_datetime(logs['timestamp'])
#         return logs
#     except Exception as e:
#         st.error(f"Error loading logs: {e}")
#         return pd.DataFrame()

# def create_metrics_row(df):
#     """Create key metrics row"""
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         total_items = len(df)
#         st.metric("Total Items", f"{total_items:,}")
    
#     with col2:
#         high_risk = len(df[df['risk_score'] > 75])
#         st.metric("High Risk Items", f"{high_risk}", delta=f"{high_risk/total_items*100:.1f}%" if total_items > 0 else 0)
    
#     with col3:
#         total_waste = df['forecasted_waste_value'].sum()
#         st.metric("Waste Value at Risk", f"₹{total_waste:,.0f}")
    
#     with col4:
#         co2_saved = df['co2_saved_kg'].sum()
#         st.metric("CO₂ Impact", f"{co2_saved:.1f} kg")

# def create_risk_distribution_chart(df):
#     """Create risk distribution chart"""
#     fig = px.histogram(
#         df, 
#         x='risk_score', 
#         nbins=20,
#         title="Risk Score Distribution",
#         labels={'risk_score': 'Risk Score', 'count': 'Number of Items'},
#         color_discrete_sequence=['#ff7f0e']
#     )
#     fig.add_vline(x=75, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
#     fig.add_vline(x=45, line_dash="dash", line_color="orange", annotation_text="Medium Risk Threshold")
#     return fig

# def create_action_recommendations_chart(df):
#     """Create action recommendations chart"""
#     action_counts = df['recommended_action'].value_counts()
    
#     fig = px.pie(
#         values=action_counts.values,
#         names=action_counts.index,
#         title="Recommended Actions Distribution",
#         color_discrete_sequence=px.colors.qualitative.Set3
#     )
#     return fig

# def create_sustainability_impact_chart(df):
#     """Create sustainability impact chart"""
#     # Top 10 items by CO2 impact
#     top_co2 = df.nlargest(10, 'co2_saved_kg')
    
#     fig = px.bar(
#         top_co2,
#         x='item_name',
#         y='co2_saved_kg',
#         title="Top 10 Items by CO₂ Impact",
#         labels={'co2_saved_kg': 'CO₂ Saved (kg)', 'item_name': 'Item Name'},
#         color='co2_saved_kg',
#         color_continuous_scale='Reds'
#     )
#     fig.update_xaxes(tickangle=45)
#     return fig

# def create_stock_vs_demand_chart(df):
#     """Create stock vs demand analysis"""
#     fig = px.scatter(
#         df,
#         x='current_stock',
#         y='predicted_daily_sales',
#         size='forecasted_waste_value',
#         color='risk_score',
#         hover_data=['item_name', 'days_remaining'],
#         title="Stock vs Demand Analysis",
#         labels={
#             'current_stock': 'Current Stock',
#             'predicted_daily_sales': 'Predicted Daily Sales',
#             'forecasted_waste_value': 'Waste Value',
#             'risk_score': 'Risk Score'
#         },
#         color_continuous_scale='RdYlGn_r'
#     )
#     return fig

# def create_timeline_chart(logs_df):
#     """Create action timeline chart"""
#     if logs_df.empty:
#         return None
    
#     # Group by date and action type
#     daily_actions = logs_df.groupby([
#         logs_df['timestamp'].dt.date, 
#         'action_type'
#     ]).size().reset_index(name='count')
    
#     fig = px.line(
#         daily_actions,
#         x='timestamp',
#         y='count',
#         color='action_type',
#         title="Daily Actions Timeline",
#         labels={'timestamp': 'Date', 'count': 'Number of Actions', 'action_type': 'Action Type'}
#     )
#     return fig

# def display_high_risk_items(df):
#     """Display high risk items table"""
#     high_risk_df = df[df['risk_score'] > 75].sort_values('risk_score', ascending=False)
    
#     if not high_risk_df.empty:
#         st.subheader("🚨 High Risk Items Requiring Immediate Attention")
        
#         # Select columns to display
#         display_cols = [
#             'item_name', 'current_stock', 'days_remaining', 'risk_score',
#             'forecasted_waste_value', 'recommended_action', 'tactical_note'
#         ]
        
#         # Filter available columns
#         available_cols = [col for col in display_cols if col in high_risk_df.columns]
        
#         st.dataframe(
#             high_risk_df[available_cols].head(10),
#             use_container_width=True,
#             hide_index=True
#         )
#     else:
#         st.info("✅ No high-risk items found!")

# def display_ai_insights():
#     """Display AI-generated insights"""
#     st.subheader("🤖 AI Insights")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         if st.button("📊 Get Daily Summary"):
#             with st.spinner("Generating summary..."):
#                 try:
#                     summary = get_daily_summary()
#                     st.write(summary)
#                 except Exception as e:
#                     st.error(f"Error generating summary: {e}")
    
#     with col2:
#         if st.button("♻️ Sustainability Optimization"):
#             with st.spinner("Analyzing sustainability..."):
#                 try:
#                     sustainability = optimize_today_for_sustainability()
#                     st.write(sustainability)
#                 except Exception as e:
#                     st.error(f"Error analyzing sustainability: {e}")
    
#     col3, col4 = st.columns(2)
    
#     with col3:
#         if st.button("📦 Return Recommendations"):
#             with st.spinner("Analyzing returns..."):
#                 try:
#                     returns = recommend_returns()
#                     st.write(returns)
#                 except Exception as e:
#                     st.error(f"Error analyzing returns: {e}")
    
#     with col4:
#         if st.button("🎯 Full Action Plan"):
#             with st.spinner("Generating action plan..."):
#                 try:
#                     action_plan = get_full_action_plan()
#                     st.write(action_plan)
#                 except Exception as e:
#                     st.error(f"Error generating action plan: {e}")

# def main():
#     """Main dashboard function"""
#     st.markdown('<h1 class="main-header">🧠 WasteWise AI Dashboard</h1>', unsafe_allow_html=True)
    
#     # Load data
#     df = load_data()
#     logs_df = load_logs()
    
#     if df.empty:
#         st.error("No data available. Please check your data files.")
#         return
    
#     # Sidebar filters
#     st.sidebar.header("🔍 Filters")
    
#     # Category filter
#     categories = ['All'] + sorted(df['category'].unique().tolist())
#     selected_category = st.sidebar.selectbox("Category", categories)
    
#     # Department filter
#     departments = ['All'] + sorted(df['department'].unique().tolist())
#     selected_department = st.sidebar.selectbox("Department", departments)
    
#     # Risk level filter
#     risk_levels = ['All', 'High Risk', 'Medium Risk', 'Low Risk']
#     selected_risk = st.sidebar.selectbox("Risk Level", risk_levels)
    
#     # Apply filters
#     filtered_df = df.copy()
    
#     if selected_category != 'All':
#         filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
#     if selected_department != 'All':
#         filtered_df = filtered_df[filtered_df['department'] == selected_department]
    
#     if selected_risk == 'High Risk':
#         filtered_df = filtered_df[filtered_df['risk_score'] > 75]
#     elif selected_risk == 'Medium Risk':
#         filtered_df = filtered_df[(filtered_df['risk_score'] > 45) & (filtered_df['risk_score'] <= 75)]
#     elif selected_risk == 'Low Risk':
#         filtered_df = filtered_df[filtered_df['risk_score'] <= 45]
    
#     # Main content
#     st.subheader(f"📈 Overview ({len(filtered_df)} items)")
    
#     # Metrics row
#     create_metrics_row(filtered_df)
    
#     # Charts section
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.plotly_chart(create_risk_distribution_chart(filtered_df), use_container_width=True)
#         st.plotly_chart(create_action_recommendations_chart(filtered_df), use_container_width=True)
    
#     with col2:
#         st.plotly_chart(create_sustainability_impact_chart(filtered_df), use_container_width=True)
#         st.plotly_chart(create_stock_vs_demand_chart(filtered_df), use_container_width=True)
    
#     # Timeline chart (full width)
#     if not logs_df.empty:
#         st.plotly_chart(create_timeline_chart(logs_df), use_container_width=True)
    
#     # High risk items section
#     display_high_risk_items(filtered_df)
    
#     # AI insights section
#     display_ai_insights()
    
#     # Data table
#     st.subheader("📋 Detailed Inventory Data")
    
#     # Column selector
#     available_cols = [
#         'item_name', 'category', 'department', 'current_stock', 
#         'days_remaining', 'risk_score', 'forecasted_waste_value',
#         'recommended_action', 'tactical_note', 'confidence'
#     ]
    
#     selected_cols = st.multiselect(
#         "Select columns to display:",
#         available_cols,
#         default=['item_name', 'category', 'current_stock', 'risk_score', 'recommended_action']
#     )
    
#     if selected_cols:
#         st.dataframe(
#             filtered_df[selected_cols],
#             use_container_width=True,
#             hide_index=True
#         )
    
#     # Footer
#     st.markdown("---")
#     st.markdown(
#         "**WasteWise AI Dashboard** | "
#         "Built with Streamlit | "
#         f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
#     )

# if __name__ == "__main__":
#     main()