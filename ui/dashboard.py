import streamlit as st
import base64
from pathlib import Path
from .components import (
    render_metrics_row,
    render_daily_chart,
    render_insights,
    render_filters,
    render_hourly_heatmap,
    render_threat_trend,
    render_country_map
)
from .styles import DASHBOARD_STYLE

def get_image_as_base64(file_path):
    """Convert image to base64 string"""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def render_dashboard(analyzer):
    st.markdown(DASHBOARD_STYLE, unsafe_allow_html=True)
    
    # Load and encode logo
    logo_path = Path(__file__).parent / "assets" / "hiya_logo.png"
    logo_base64 = get_image_as_base64(logo_path)
    
    # Header with larger logo
    st.markdown(f"""
    <div class="main-header">
        <img src="data:image/png;base64,{logo_base64}" 
             class="logo-image">
        <h1>Spam Protection Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)

    date_range, call_types = render_filters(analyzer)
    render_metrics_row(analyzer)
    st.markdown("---")
    
    # Daily analysis
    st.markdown("### 📊 Daily Analysis")
    render_daily_chart(analyzer.get_daily_stats())
    
    # New visualizations in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⏰ Hourly Patterns")
        render_hourly_heatmap(analyzer)
        
    with col2:
        st.markdown("### 📈 Threat Trends")
        render_threat_trend(analyzer)
    
    # Geographic analysis
    st.markdown("### 🌍 Geographic Analysis")
    render_country_map(analyzer)
    
    # Insights
    render_insights(analyzer)