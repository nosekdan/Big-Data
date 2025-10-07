# indexer.py
import re
import json
from pathlib import Path
from repository_connection import collection, client

# ----------------------
# CONTROL FILES SETUP
# ----------------------
INDEXED_FILE = Path("./control/indexed_books.txt")
DOWNLOADS_FILE = Path("./control/downloaded_books.txt")

# ----------------------
# TOKENIZER
# ----------------------
def tokenize(text: str):
    """Simple tokenizer: lowercase, only words of 2+ letters."""
    return re.findall(r"\b[a-z]{2,}\b", text.lower())
  
# ----------------------
# MongoDB Update
# ----------------------
def update_fs(term: str, book_id: int):
    """Store postings list for one term in its own file under its first letter folder."""
    first_letter = term[0].lower()
    index_db = client["invertedIndex"]
    collection = index_db[first_letter]  # Collection for the first letter

    # Try to find the document for the term
    doc = collection.find_one({"term": term})

    if doc:
        # Term exists, update postings if book_id not already present
        if book_id not in doc["postings"]:
            collection.update_one(
                {"term": term},
                {"$push": {"postings": book_id}}
            )
    else:
        # Term doesn't exist, create new document
        collection.insert_one({
            "term": term,
            "postings": [book_id]
        })

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
    # Indexing all books once at the start
    reindex_all_books()
    # Watching for changes in the books collection
    with collection.watch([{"$match": {"operationType": {"$ne": "delete"}}}]) as stream:
        print("Watching for changes in the 'books' collection...")
        for change in stream:
            print("Change detected!")
            reindex_all_books()
            print("🎉 Indexing complete.")
            print("Watching for changes in the 'books' collection...")
