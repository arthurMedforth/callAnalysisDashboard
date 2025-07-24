import streamlit as st
from .components import (
    render_metrics_row,
    render_daily_chart,
    render_insights,
    render_filters
)
from .styles import DASHBOARD_STYLE

def render_dashboard(callAnalysis):
    st.markdown(DASHBOARD_STYLE, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Hiya Spam Protection Dashboard</h1>
        <h3>Monthly Performance Report - May 2024</h3>
    </div>
    """, unsafe_allow_html=True)

    date_range, call_types = render_filters(callAnalysis)
    render_metrics_row(callAnalysis)
    st.markdown("---")
    render_daily_chart(callAnalysis.get_daily_stats())
    render_insights(callAnalysis)