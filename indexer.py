# indexer.py
import os
import re
import json
import sqlite3
from pathlib import Path
from pymongo import MongoClient
from repository_connection import collection  # reuses your MongoDB "books" collection

# ----------------------
# PATHS & CONTROL FILES
# ----------------------
CONTROL_DIR = Path("control")
CONTROL_DIR.mkdir(parents=True, exist_ok=True)

INDEXED_FILE = CONTROL_DIR / "indexed_books.txt"

# ----------------------
# DATABASE SETUP
# ----------------------

# SQLite (datamart 1)
sql_conn = sqlite3.connect("datamarts/inverted_index.db")
sql_cur = sql_conn.cursor()
sql_cur.execute("""
CREATE TABLE IF NOT EXISTS inverted_index (
    term TEXT PRIMARY KEY,
    postings TEXT -- JSON array of book_ids
)
""")
sql_conn.commit()

# MongoDB (datamart 2)
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["BigData"]
mongo_index = mongo_db["inverted_index"]
mongo_index.create_index("term", unique=True)

# ----------------------
# TOKENIZER
# ----------------------
def tokenize(text: str):
    """Simple tokenizer: lowercase, only words of 2+ letters."""
    return re.findall(r"\b[a-z]{2,}\b", text.lower())

# ----------------------
# UPDATE FUNCTIONS
# ----------------------
def update_sql(term, book_id):
    sql_cur.execute("SELECT postings FROM inverted_index WHERE term=?", (term,))
    row = sql_cur.fetchone()
    if row:
        postings = json.loads(row[0])
        if book_id not in postings:
            postings.append(book_id)
            sql_cur.execute("UPDATE inverted_index SET postings=? WHERE term=?",
                            (json.dumps(postings), term))
    else:
        sql_cur.execute("INSERT INTO inverted_index (term, postings) VALUES (?, ?)",
                        (term, json.dumps([book_id])))

def update_mongo(term, book_id):
    mongo_index.update_one(
        {"term": term},
        {"$addToSet": {"postings": book_id}},
        upsert=True
    )

# ----------------------
# INDEXING LOGIC
# ----------------------
def process_book(book_id: int, text: str):
    words = set(tokenize(text))
    sql_cur.execute("BEGIN TRANSACTION")
    for term in words:
        update_sql(term, book_id)
        update_mongo(term, book_id)
    sql_conn.commit()
    mark_indexed(book_id)
    print(f"✅ Indexed book {book_id} ({len(words)} unique terms).")

def mark_indexed(book_id: int):
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
            continue
        text = doc["content"]
        process_book(book_id, text)

if __name__ == "__main__":
    reindex_all_books()
    print("🎉 Indexing complete.")
