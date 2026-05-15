import streamlit as st
import plotly.express as px
import pandas as pd

def show_top_senders(result):
    st.header("Top Email Senders")
    
    if not result.top_senders:
        st.info("No sender data available")
        return
    
    # Data table
    df = pd.DataFrame(result.top_senders)
    st.dataframe(
        df[["rank", "email", "name", "count", "percentage"]].rename(columns={
            "rank": "Rank",
            "email": "Email",
            "name": "Sender Name",
            "count": "Email Count",
            "percentage": "% of Total"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Bar chart
    fig = px.bar(
        df, x="email", y="count",
        title="Top Senders by Email Count",
        labels={"email": "Email", "count": "Count"},
        color="count"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Download top senders CSV
    from src.core.export import generate_top_senders_csv
    csv = generate_top_senders_csv(result.top_senders)
    st.download_button(
        label="Download Top Senders CSV",
        data=csv,
        file_name="top_senders.csv",
        mime="text/csv"
    )
