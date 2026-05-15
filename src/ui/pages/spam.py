import streamlit as st
import plotly.express as px
import pandas as pd

def show_spam(result):
    st.header("Spam Detection Results")
    st.metric("Total Spam Emails", result.spam_count)
    
    if not result.emails:
        st.info("No email data available")
        return
    
    # Filter spam emails
    spam_emails = [e for e in result.emails if e.is_spam]
    
    if not spam_emails:
        st.info("No spam emails detected")
        return
    
    # Data table
    df = pd.DataFrame([{
        "Date": e.date.strftime("%Y-%m-%d %H:%M") if e.date else "",
        "Sender": e.sender_email,
        "Subject": e.subject or "",
        "Confidence": f"{e.spam_confidence:.2f}",
        "Reasons": "; ".join(e.spam_reasons) if e.spam_reasons else ""
    } for e in spam_emails])
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Confidence distribution
    st.subheader("Spam Confidence Distribution")
    conf_df = pd.DataFrame([{"Confidence": e.spam_confidence} for e in spam_emails])
    if not conf_df.empty:
        fig = px.histogram(conf_df, x="Confidence", nbins=10, title="Spam Confidence Scores")
        st.plotly_chart(fig, use_container_width=True)
