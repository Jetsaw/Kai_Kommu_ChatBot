# tools/update_sop.py
import os, sys, json
# >>> add these 3 lines <<<
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dotenv import load_dotenv
load_dotenv()

from sop_doc_loader import fetch_sop_doc_text, parse_qas_from_text
from config import RAG_DIR, SOP_JSON_PATH

def main():
    os.makedirs(RAG_DIR, exist_ok=True)
    txt = fetch_sop_doc_text()
    qas = parse_qas_from_text(txt)
    print(f"[update_sop] Parsed {len(qas)} Q/A")
    with open(SOP_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(qas, f, ensure_ascii=False, indent=2)
    print(f"[update_sop] Wrote {len(qas)} Q/A → {SOP_JSON_PATH}")

if __name__ == "__main__":
    main()
