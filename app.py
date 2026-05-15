import streamlit as st
import pandas as pd
import tempfile
import os

from src import analyze_mbox, generate_csv_content, Settings

st.set_page_config(
    page_title="MBOX Analyzer",
    page_icon="📧",
    layout="wide"
)

st.title("📧 MBOX Email Analyzer")
st.markdown("Upload your `.mbox` file (from Google Takeout) to analyze top email senders.")

# Sidebar & File Upload
with st.sidebar:
    st.header("📂 Data Source")
    uploaded_file = st.file_uploader(
        "Choose a .mbox file",
        type=["mbox", "mbx"],
        help="Maximum file size depends on your Streamlit config"
    )
    
    st.markdown("---")
    st.header("⚙️ Settings")
    top_n = st.number_input(
        "Number of top senders to show",
        min_value=Settings.MIN_TOP_N,
        max_value=Settings.MAX_TOP_N,
        value=Settings.DEFAULT_TOP_N,
        step=5
    )
    st.markdown("---")
    st.markdown("**How to get .mbox file:**")
    st.markdown("1. Go to [Google Takeout](https://takeout.google.com)")
    st.markdown("2. Select 'Mail' and export as .mbox")

# Main Logic
if uploaded_file is not None:
    tmp_path = None
    try:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mbox") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with st.spinner("Analyzing emails... This may take a while for large files."):
            results = analyze_mbox(tmp_path, top_n=top_n)

        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Emails", f"{results['total']:,}")
        col2.metric("Unique Senders", f"{len(results['sender_counter']):,}")
        col3.metric("Processing Errors", f"{results['errors']:,}")

        if results["total"] == 0:
            st.error("No emails found in the uploaded file.")
            st.stop()

        # Prepare top senders data for display
        top_data = []
        for rank, (email, count) in enumerate(results["top_senders"], 1):
            pct = count / results["total"] * 100
            name = results["sender_names"].get(email, "")
            top_data.append({
                "Rank": rank,
                "Email": email,
                "Name": name,
                "Count": count,
                "Percentage (%)": round(pct, 2)
            })

        df = pd.DataFrame(top_data)

        # Display table
        st.subheader(f"🏆 Top {top_n} Senders")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # Bar chart
        st.subheader("📊 Sender Distribution")
        chart_data = df.set_index("Email")["Count"].head(top_n)
        st.bar_chart(chart_data)

        # CSV download
        st.subheader("📥 Export Results")
        csv_content = generate_csv_content(
            results["sender_counter"],
            results["sender_names"],
            results["total"]
        )
        st.download_button(
            label="Download Full CSV Report",
            data=csv_content,
            file_name="mbox_analysis_results.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
    finally:
        # Clean up temp file
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
