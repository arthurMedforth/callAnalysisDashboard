import streamlit as st
import os
from src.call_data_analyzer import CallDataAnalyzer
from ui.dashboard import render_dashboard

def main():
    st.set_page_config(
        page_title="Hiya Spam Protection Dashboard",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # File upload section
    st.sidebar.header("📁 Data Input")
    uploaded_file = st.sidebar.file_uploader(
        "Upload your Excel file",
        type=['xlsx', 'xls'],
        accept_multiple_files=False,
        help="Upload an Excel file containing call data",
        key='uploaded_file'
    )

    if uploaded_file is not None:
        with st.spinner('Processing file...'):
            try:
                # Clear any cached data
                st.cache_data.clear()
                
                # Create new analyzer instance
                analyzer = CallDataAnalyzer(uploaded_file)
                render_dashboard(analyzer)
                st.sidebar.success('File processed successfully!')
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                st.info("""
                    Please ensure your Excel file contains the required columns:
                    - date (datetime)
                    - calling phone number (string/integer)
                    - flagged (categorical: neutral, spam, fraud)
                """)
    else:
        # Show welcome message
        st.markdown("""
        # 👋 Welcome to Hiya Spam Protection Dashboard
        
        Please upload your Excel file using the sidebar to get started.
        
        ### Required Data Format:
        Your Excel file should contain these columns:
        - `date`: Date of the call
        - `calling phone number`: Phone number of caller
        - `flagged`: Call classification (neutral/spam/fraud)
        """)

if __name__ == "__main__":
    main()