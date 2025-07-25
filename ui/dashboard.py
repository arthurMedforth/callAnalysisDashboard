import streamlit as st
from .components import (
    render_metrics_row,
    render_daily_chart,
    render_insights,
    render_filters
)
from .styles import DASHBOARD_STYLE

def render_dashboard(analyzer):
    st.markdown(DASHBOARD_STYLE, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Hiya Spam Protection Dashboard</h1>
        <h3>Call Protection Performance Report</h3>
    </div>
    """, unsafe_allow_html=True)

    date_range, call_types = render_filters(analyzer)
    render_metrics_row(analyzer)
    st.markdown("---")
    render_daily_chart(analyzer.get_daily_stats())
    render_insights(analyzer)