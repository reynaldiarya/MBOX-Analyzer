# MBOX Analyzer

Analyze your email .mbox files (from Google Takeout) to find top senders, with a web interface.

## Features
- Upload .mbox files via web interface
- View top email senders with statistics
- Interactive bar chart visualization
- Export full results to CSV

## Prerequisites
- Python 3.8+
- Existing `.venv` with dependencies installed

## How to Run

1. Activate the virtual environment:
```powershell
.venv\Scripts\Activate.ps1
```

2. Run the Streamlit app:
```powershell
streamlit run streamlit_app.py
```

3. Open the URL shown in the terminal (usually http://localhost:8501)

## How to Get .mbox File
1. Go to [Google Takeout](https://takeout.google.com)
2. Select "Mail" and choose .mbox format
3. Export and download the archive
4. Extract the .mbox file and upload it to the app

## Dependencies
- streamlit
- pandas
- (Standard library modules: mailbox, re, csv, etc.)
