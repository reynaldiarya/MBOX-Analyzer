import streamlit as st
import plotly.express as px
import pandas as pd


def show_timeline(result):
    st.header("Sender Timeline Analytics")

    if not result.timeline_data:
        st.info("No timeline data available")
        return

    # Time grouping toggle
    time_group = st.radio("Group By", ["Daily", "Weekly", "Monthly"], horizontal=True)

    # Convert to DataFrame
    df = pd.DataFrame(result.timeline_data)
    df["date"] = pd.to_datetime(df["date"])

    # Resample based on selection
    if time_group == "Weekly":
        df.set_index("date", inplace=True)
        df = df.resample("W").sum().reset_index()
    elif time_group == "Monthly":
        df.set_index("date", inplace=True)
        df = df.resample("ME").sum().reset_index()

    # Line chart
    fig = px.line(
        df,
        x="date",
        y="count",
        title=f"Email Volume ({time_group})",
        labels={"date": "Date", "count": "Email Count"},
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Data table
    st.subheader("Timeline Data")
    st.dataframe(
        df.rename(columns={"date": "Date", "count": "Email Count"}),
        use_container_width=True,
        hide_index=True,
    )
