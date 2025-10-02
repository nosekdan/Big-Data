# indexer.py
import re
import json
from pathlib import Path
from repository_connection import collection

# ----------------------
# FILESYSTEM INDEX SETUP
# ----------------------
FS_DIR = Path("../database")
FS_DIR.mkdir(parents=True, exist_ok=True)

INDEXED_FILE = Path("../database/indexed_books.txt")

# ----------------------
# TOKENIZER
# ----------------------
def tokenize(text: str):
    """Simple tokenizer: lowercase, only words of 2+ letters."""
    return re.findall(r"\b[a-z]{2,}\b", text.lower())
  
# ----------------------
# FILESYSTEM UPDATE
# ----------------------
def update_fs(term: str, book_id: int):
    """Store postings list for one term in its own file under its first letter folder."""
    first_letter = term[0].lower()
    subdir = FS_DIR / first_letter
    subdir.mkdir(parents=True, exist_ok=True)

    file_path = subdir / f"{term}.json"

    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            postings = json.load(f)["postings"]
    else:
        postings = []

    if book_id not in postings:
        postings.append(book_id)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"term": term, "postings": postings}, f, indent=2)

# ----------------------
# INDEXING LOGIC
# ----------------------
def process_book(book_id: int, text: str):
    words = set(tokenize(text))
    for term in words:
        update_fs(term, book_id)
    mark_indexed(book_id)
    print(f"✅ Indexed book {book_id} ({len(words)} unique terms).")

def mark_indexed(book_id: int):
    INDEXED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEXED_FILE, "a", encoding="utf-8") as f:
        f.write(f"{book_id}\n")

def already_indexed(book_id: int) -> bool:
    if not INDEXED_FILE.exists():
        return False
    with open(INDEXED_FILE, "r", encoding="utf-8") as f:
        return str(book_id) in f.read().splitlines()

# ----------------------
# MAIN
# ----------------------
def reindex_all_books():
    """Index all books from the MongoDB books collection."""
    for doc in collection.find():
        book_id = doc["id"]
        if already_indexed(book_id):
            print(f"⚠️  Book {book_id} already indexed, skipping.")
            continue
        text = doc["content"]
        process_book(book_id, text)

if __name__ == "__main__":
  #TODO: event driven, by a change in the database
    reindex_all_books()
    print("🎉 Indexing complete.")
