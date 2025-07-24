import streamlit as st
from src.call_data_analyzer import CallDataAnalyzer
from ui.dashboard import render_dashboard

def main():
    st.set_page_config(
        page_title="Hiya Spam Protection Dashboard",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    callDataAnalysis = CallDataAnalyzer("Example call data.xlsx")
    render_dashboard(callDataAnalysis)

if __name__ == "__main__":
    main()