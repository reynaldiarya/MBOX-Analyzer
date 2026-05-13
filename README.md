# Paling simpel (akan minta path interaktif)
python analyze_mbox.py

# Langsung kasih path file
python analyze_mbox.py "/path/ke/inbox.mbox"

# Tampilkan top 30, sekalian export ke CSV
python analyze_mbox.py inbox.mbox --top 30 --export hasil.csv