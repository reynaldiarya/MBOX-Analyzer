import streamlit as st
import tempfile
import os
from datetime import datetime
from src.core.config import Settings
from src.core.analyzer import analyze_mbox
from src.core.export import generate_csv_content
from src.ui import (
    show_overview, show_top_senders, show_top_domains,
    show_timeline, show_spam, show_newsletters
)

st.set_page_config(
    page_title="MBOX Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if "analytics_result" not in st.session_state:
    st.session_state.analytics_result = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None
if "temp_file_path" not in st.session_state:
    st.session_state.temp_file_path = None
if "current_filters" not in st.session_state:
    st.session_state.current_filters = {}

# Sidebar navigation
st.sidebar.title("MBOX Analyzer")

# File upload at the very top
st.sidebar.header("Upload MBOX")
uploaded_file = st.sidebar.file_uploader(
    "Choose .mbox file",
    type=["mbox", "mbx"],
    help="Upload your MBOX file for analysis"
)

# Process uploaded file
if uploaded_file is not None:
    if uploaded_file.name != st.session_state.uploaded_file_name:
        settings = Settings()  # Initialize settings here
        # Save new file
        if st.session_state.temp_file_path and os.path.exists(st.session_state.temp_file_path):
            os.unlink(st.session_state.temp_file_path)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mbox") as tmp:
            tmp.write(uploaded_file.read())
            st.session_state.temp_file_path = tmp.name
        
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.current_filters = {}
        
        # Run initial analysis
        with st.spinner("Analyzing MBOX file..."):
            result = analyze_mbox(st.session_state.temp_file_path, top_n=settings.DEFAULT_TOP_N)
            st.session_state.analytics_result = result
            st.session_state.current_filters = {
                "top_n": settings.DEFAULT_TOP_N,
                "date_range": "[]",
                "sender_filter": "[]",
                "domain_filter": "[]"
            }
        st.rerun()

# Sidebar filters (only show if file is uploaded)
if st.session_state.temp_file_path and os.path.exists(st.session_state.temp_file_path):
    st.sidebar.header("Filters")
    settings = Settings()
    
    top_n = st.sidebar.number_input(
        "Top N Results",
        min_value=settings.MIN_TOP_N,
        max_value=settings.MAX_TOP_N,
        value=settings.DEFAULT_TOP_N,
        key="top_n_input"
    )
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[],
        help="Filter emails by date range"
    )
    
    # Dynamic sender/domain filters
    sender_options = []
    domain_options = []
    if st.session_state.analytics_result:
        result = st.session_state.analytics_result
        sender_options = sorted(list({e.sender_email for e in result.emails}))
        domain_options = sorted(list({e.sender_domain for e in result.emails if e.sender_domain}))
    
    sender_filter = st.sidebar.multiselect("Filter by Sender", options=sender_options, key="sender_filter")
    domain_filter = st.sidebar.multiselect("Filter by Domain", options=domain_options, key="domain_filter")
    
    # Check if filters changed and re-run analysis
    new_filters = {
        "top_n": top_n,
        "date_range": str(date_range),
        "sender_filter": str(sender_filter),
        "domain_filter": str(domain_filter)
    }
    
    if new_filters != st.session_state.current_filters:
        with st.spinner("Applying filters..."):
            dt_range = None
            if len(date_range) == 2:
                dt_range = (
                    datetime.combine(date_range[0], datetime.min.time()),
                    datetime.combine(date_range[1], datetime.max.time())
                )
            result = analyze_mbox(
                st.session_state.temp_file_path,
                top_n=top_n,
                date_range=dt_range,
                sender_filter=sender_filter if sender_filter else None,
                domain_filter=domain_filter if domain_filter else None
            )
            st.session_state.analytics_result = result
            st.session_state.current_filters = new_filters
    
    # CSV download
    if st.session_state.analytics_result:
        csv_content = generate_csv_content(st.session_state.analytics_result)
        st.sidebar.download_button(
            label="Download Full CSV Report",
            data=csv_content,
            file_name=f"mbox_analysis_{st.session_state.uploaded_file_name or 'report'}.csv",
            mime="text/csv"
        )

# Navigation (only show if analysis done)
if st.session_state.analytics_result is None:
    st.info("Please upload an MBOX file to start analysis.")
else:
    nav_option = st.sidebar.radio(
        "Navigate",
        ["Overview", "Top Senders", "Top Domains", "Timeline", "Spam Detection", "Newsletters"]
    )
    
    result = st.session_state.analytics_result
    page_functions = {
        "Overview": show_overview,
        "Top Senders": show_top_senders,
        "Top Domains": show_top_domains,
        "Timeline": show_timeline,
        "Spam Detection": show_spam,
        "Newsletters": show_newsletters
    }
    page_functions[nav_option](result)
