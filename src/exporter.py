import csv
import io
from collections import Counter

def generate_csv_content(counter: Counter, names: dict, total: int) -> str:
    """
    Generate CSV content as string for download.
    Args:
        counter: Sender Counter object
        names: Dict mapping email → name
        total: Total emails analyzed
    Returns:
        CSV content as string (UTF-8 with BOM for Excel compatibility)
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Rank", "Email", "Nama", "Jumlah Email", "% dari Total"])

    for rank, (email_addr, count) in enumerate(counter.most_common(), 1):
        pct = f"{count / total * 100:.2f}%"
        name = names.get(email_addr, "")
        writer.writerow([rank, email_addr, name, count, pct])

    # Add BOM for Excel compatibility
    return "\ufeff" + output.getvalue()
