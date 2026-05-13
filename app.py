"""
TOP EMAIL SENDERS ANALYZER - dari file .mbox (Google Takeout)
==============================================================
Cara pakai:
  1. Install Python 3 (https://python.org) jika belum ada
  2. Jalankan: python analyze_mbox.py
  3. Masukkan path ke file .mbox saat diminta

Atau langsung dengan argumen:
  python analyze_mbox.py inbox.mbox
  python analyze_mbox.py inbox.mbox --top 30
  python analyze_mbox.py inbox.mbox --top 30 --export hasil.csv
"""

import mailbox
import re
import sys
import csv
import os
import argparse
from collections import Counter
from email.header import decode_header
from email.utils import parseaddr


# ─── KONFIGURASI ──────────────────────────────────────────────────────────────

DEFAULT_TOP_N   = 20      # Tampilkan N pengirim teratas
PROGRESS_EVERY  = 1000    # Tampilkan progress setiap N email


# ─── FUNGSI UTAMA ─────────────────────────────────────────────────────────────

def decode_str(value: str) -> str:
    """Decode encoded email header (misalnya =?UTF-8?B?...?=)."""
    if not value:
        return ""
    parts = decode_header(value)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try:
                decoded.append(part.decode(charset or "utf-8", errors="replace"))
            except Exception:
                decoded.append(part.decode("latin-1", errors="replace"))
        else:
            decoded.append(part)
    return "".join(decoded).strip()


def parse_sender(from_header: str) -> tuple[str, str]:
    """
    Ekstrak nama dan email dari header From.
    Contoh: '"John Doe" <john@example.com>' → ('John Doe', 'john@example.com')
    """
    decoded = decode_str(from_header)
    name, email_addr = parseaddr(decoded)
    email_addr = email_addr.lower().strip()

    # Fallback: coba cari email dengan regex jika parseaddr gagal
    if not email_addr or "@" not in email_addr:
        match = re.search(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", decoded)
        email_addr = match.group(0).lower() if match else decoded.lower()
        name = ""

    return name.strip('"').strip(), email_addr


def analyze_mbox(mbox_path: str, top_n: int = DEFAULT_TOP_N, export_csv: str = None):
    """Analisis .mbox dan tampilkan top pengirim."""

    if not os.path.exists(mbox_path):
        print(f"❌ File tidak ditemukan: {mbox_path}")
        sys.exit(1)

    file_size_mb = os.path.getsize(mbox_path) / (1024 * 1024)
    print(f"\n📂 File  : {mbox_path}")
    print(f"📦 Ukuran: {file_size_mb:.1f} MB")
    print(f"🔍 Memulai analisis...\n")

    mbox = mailbox.mbox(mbox_path)

    sender_counter: Counter = Counter()
    sender_names: dict[str, str] = {}   # email → nama terbaru
    total = 0
    errors = 0

    for i, message in enumerate(mbox):
        try:
            from_header = message.get("From", "")
            if not from_header:
                continue

            name, email_addr = parse_sender(from_header)
            if not email_addr:
                continue

            sender_counter[email_addr] += 1
            if name and email_addr not in sender_names:
                sender_names[email_addr] = name

            total += 1

            if total % PROGRESS_EVERY == 0:
                print(f"  → Diproses: {total:,} email...", end="\r")

        except Exception as e:
            errors += 1

    print(f"  → Diproses: {total:,} email... selesai!    ")

    if total == 0:
        print("❌ Tidak ada email ditemukan di file ini.")
        return

    # ─── Tampilkan hasil ──────────────────────────────────────────────────────

    top_senders = sender_counter.most_common(top_n)

    print(f"\n{'─'*70}")
    print(f"🏆  TOP {top_n} PENGIRIM EMAIL TERBANYAK")
    print(f"{'─'*70}")
    print(f"{'No.':<5} {'Email':<38} {'Jumlah':>7}  {'%':>6}  Bar")
    print(f"{'─'*70}")

    for rank, (email_addr, count) in enumerate(top_senders, 1):
        pct   = count / total * 100
        bar   = "█" * max(1, round(pct / 1.5))
        name  = sender_names.get(email_addr, "")
        label = f"{email_addr}" + (f"  ({name})" if name else "")
        label = label[:50]
        print(f"{rank:<5} {label:<38} {count:>7,}  {pct:>5.1f}%  {bar}")

    print(f"{'─'*70}")
    print(f"📬 Total email dianalisis  : {total:,}")
    print(f"👥 Total pengirim unik     : {len(sender_counter):,}")
    if errors:
        print(f"⚠️  Email gagal diproses   : {errors:,}")

    # ─── Export CSV (opsional) ────────────────────────────────────────────────

    if export_csv:
        export_results(sender_counter, sender_names, total, export_csv)

    print(f"\n💡 Tip: tambahkan --export hasil.csv untuk simpan semua data ke CSV.")


def export_results(counter: Counter, names: dict, total: int, csv_path: str):
    """Ekspor seluruh data ke file CSV."""
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Email", "Nama", "Jumlah Email", "% dari Total"])
        for rank, (email_addr, count) in enumerate(counter.most_common(), 1):
            pct = f"{count / total * 100:.2f}%"
            name = names.get(email_addr, "")
            writer.writerow([rank, email_addr, name, count, pct])

    print(f"\n✅ Data diekspor ke: {csv_path}  ({len(counter):,} pengirim unik)")


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Analisis top pengirim email dari file .mbox (Google Takeout)"
    )
    parser.add_argument(
        "mbox_file",
        nargs="?",
        help="Path ke file .mbox (opsional, akan diminta jika tidak diberikan)"
    )
    parser.add_argument(
        "--top", "-t",
        type=int,
        default=DEFAULT_TOP_N,
        metavar="N",
        help=f"Tampilkan N pengirim teratas (default: {DEFAULT_TOP_N})"
    )
    parser.add_argument(
        "--export", "-e",
        metavar="FILE.csv",
        help="Ekspor semua hasil ke file CSV"
    )

    args = parser.parse_args()

    mbox_path = args.mbox_file
    if not mbox_path:
        mbox_path = input("📁 Masukkan path ke file .mbox: ").strip().strip("'\"")

    analyze_mbox(mbox_path, top_n=args.top, export_csv=args.export)


if __name__ == "__main__":
    main()