import streamlit as st
import plotly.express as px
import pandas as pd

def show_top_domains(result):
    st.header("Top Email Domains")
    
    if not result.top_domains:
        st.info("No domain data available")
        return
    
    # Data table
    df = pd.DataFrame(result.top_domains)
    st.dataframe(
        df[["rank", "domain", "count", "percentage"]].rename(columns={
            "rank": "Rank",
            "domain": "Domain",
            "count": "Email Count",
            "percentage": "% of Total"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Bar chart
    fig = px.bar(
        df, x="domain", y="count",
        title="Top Domains by Email Count",
        labels={"domain": "Domain", "count": "Count"},
        color="count"
    )
    st.plotly_chart(fig, use_container_width=True)
