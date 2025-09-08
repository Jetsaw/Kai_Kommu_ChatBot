import json, os
from pathlib import Path

SOP_JSON = Path("rag/sop_data.json")

NEW_QAS = [
    # English
    {"question":"What is Kommu?","answer":"Kommu builds KommuAssist, a Level 2 driver-assistance (ADAS) upgrade for compatible cars. It adds lane centering, adaptive cruise control (ACC), and stop-and-go via plug-and-play hardware. Learn more: https://kommu.ai/"},
    {"question":"How does Kommu work?","answer":"KommuAssist uses plug-and-play hardware running a driver-assistance model tuned for Malaysian roads. It keeps the car centered, maintains distance (ACC), and handles stop-and-go. Details: https://kommu.ai/"},
    {"question":"Is Kommu safe? Will it void warranty?","answer":"KommuAssist is an assistance system (not autonomous driving). The driver must remain alert. Installation is non-destructive and reversible; original safety systems remain. Read more: https://kommu.ai/faq/"},
    {"question":"Which cars are supported by Kommu?","answer":"Compatibility depends on make, model, year, and ADAS packages (ACC/LKAS). Many Perodua, Proton, Honda, and Toyota models are targeted. Check latest status: https://kommu.ai/support/"},
    {"question":"How do I buy Kommu?","answer":"Order KommuAssist 1s here: https://kommu.ai/products/ (ships ~1 week; free install at HQ by appointment)."},
    {"question":"How much does Kommu cost?","answer":"See the current price on the product page: https://kommu.ai/products/ . Share your car make/model/year/trim and whether it has ACC/LKAS if you’d like suitability confirmed first."},
    {"question":"Can I book a test drive?","answer":"Yes. Book a test drive here: https://calendly.com/kommuassist/test-drive?month=2025-08"},
    {"question":"Where is Kommu located? What are the office hours?","answer":"Office hours: Monday–Friday, 10:00–18:00 (MYT). Address: C/105B, Block C, Jalan PJU 10/2a, Damansara Damai, 47830 Petaling Jaya, Selangor. Waze: https://waze.com/ul?ll=3.2137,101.6056&navigate=yes"},
    # BM
    {"question":"Apa itu Kommu?","answer":"Kommu menghasilkan KommuAssist, sistem bantuan pemanduan Tahap 2 (ADAS) untuk kereta yang serasi. Ia menambah pengekalan lorong, kawalan jelajah adaptif (ACC) dan stop-and-go melalui perkakasan plug-and-play. Maklumat: https://kommu.ai/"},
    {"question":"Bagaimana Kommu berfungsi?","answer":"KommuAssist menggunakan perkakasan plug-and-play yang menjalankan model bantuan pemanduan ditala untuk jalan raya Malaysia. Ia mengekalkan kereta di tengah lorong, mengekalkan jarak (ACC), dan mengendalikan trafik henti-gerak. Butiran: https://kommu.ai/"},
    {"question":"Boleh saya tempah pandu uji?","answer":"Boleh. Tempah pandu uji di sini: https://calendly.com/kommuassist/test-drive?month=2025-08"}
]

def load_existing():
    if SOP_JSON.exists():
        with open(SOP_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def dedupe_merge(old, new):
    by_q = { item["question"].strip(): item for item in old if "question" in item and "answer" in item }
    for item in new:
        q = item.get("question","").strip()
        a = item.get("answer","").strip()
        if not q or not a:
            continue
        by_q[q] = {"question": q, "answer": a}
    return list(by_q.values())

def main():
    old = load_existing()
    merged = dedupe_merge(old, NEW_QAS)
    os.makedirs(SOP_JSON.parent, exist_ok=True)
    with open(SOP_JSON, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"Merged {len(NEW_QAS)} new entries. Total Q/A now: {len(merged)}")
    print(f"→ {SOP_JSON.resolve()}")

if __name__ == "__main__":
    main()
