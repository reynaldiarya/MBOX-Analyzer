import streamlit as st
import plotly.express as px


def show_overview(result):
    st.header("Dashboard Overview")

    # Metrics cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Emails", result.total_emails)
    with col2:
        st.metric("Unique Senders", result.unique_senders)
    with col3:
        st.metric("Spam Emails", result.spam_count)
    with col4:
        st.metric("Newsletters", result.newsletter_count)
    with col5:
        st.metric("Processing Errors", result.errors)

    # Top Senders Chart
    st.subheader("Top Senders")
    if result.top_senders:
        df = [{"Email": s["email"], "Count": s["count"]} for s in result.top_senders]
        fig = px.bar(df, x="Email", y="Count", title="Top Email Senders", color="Count")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No sender data available")

    # Top Domains Chart
    st.subheader("Top Domains")
    if result.top_domains:
        df = [{"Domain": d["domain"], "Count": d["count"]} for d in result.top_domains]
        fig = px.bar(
            df, x="Domain", y="Count", title="Top Email Domains", color="Count"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No domain data available")
