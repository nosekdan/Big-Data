import re
import json
from pathlib import Path

# ----------------------
# FILESYSTEM INDEX SETUP
# ----------------------
FS_DIR = Path("../database")
FS_DIR.mkdir(parents=True, exist_ok=True)
            
# ----------------------
# FILESYSTEM SEARCH
# ----------------------

def search_fs(term: str):
    """Return postings for a term if it exists in filesystem index."""
    first_letter = term[0].lower()
    file_path = FS_DIR / first_letter / f"{term}.json"
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)["postings"]
      
if __name__ == "__main__":
    term = input("Enter search term: ").strip().lower()
    # mehrere Suchbegriffe trennen (z.B. durch Leerzeichen)
    terms = term.split()
    if terms:
        postings = set(search_fs(terms[0]))  # Annahme: search_fs gibt eine Liste von Indexen zurück
        # weitere Terme nacheinander schneiden
        for t in terms[1:]:
            postings &= set(search_fs(t))  # Schnittmenge bilden

        if postings:
            print(f"Found in books: {sorted(postings)}")
        else:
            print("No results found.")
    else:
        print("No input provided.")
    print("🎉 Search complete.")