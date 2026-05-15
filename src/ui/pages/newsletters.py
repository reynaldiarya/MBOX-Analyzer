import streamlit as st
import plotly.express as px
import pandas as pd

def show_newsletters(result):
    st.header("Newsletter Detection Results")
    st.metric("Total Newsletters", result.newsletter_count)
    
    if not result.emails:
        st.info("No email data available")
        return
    
    # Filter newsletter emails
    newsletter_emails = [e for e in result.emails if e.is_newsletter]
    
    if not newsletter_emails:
        st.info("No newsletters detected")
        return
    
    # Data table
    df = pd.DataFrame([{
        "Date": e.date.strftime("%Y-%m-%d %H:%M") if e.date else "",
        "Sender": e.sender_email,
        "Subject": e.subject or "",
        "Platform": e.newsletter_platform or "Unknown",
        "Confidence": f"{e.newsletter_confidence:.2f}"
    } for e in newsletter_emails])
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Platform distribution
    st.subheader("Newsletter Platforms")
    platform_counts = df["Platform"].value_counts().reset_index()
    platform_counts.columns = ["Platform", "Count"]
    if not platform_counts.empty:
        fig = px.pie(platform_counts, values="Count", names="Platform", title="Newsletters by Platform")
        st.plotly_chart(fig, use_container_width=True)
