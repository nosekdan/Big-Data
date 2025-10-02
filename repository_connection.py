from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["BigData"]
collection = db["books"]

def connect_to_db():
    try:
        info = client.server_info()  # Force connection on a request as the connect=True parameter of MongoClient seems to be useless here
        print("✅ Successfully connected to MongoDB!")
        print("MongoDB version:", info["version"])
    except ConnectionFailure as e:
        print("❌ Could not connect to MongoDB:", e)


def insert_into_db(books):
    if not books:
        print("No books to insert.")
        return
    for book in books:
        if collection.find_one({"id": book[0]}):
            print(f"⚠️ Book with ID {book[0]} already exists in the database, deleting the old entry.")
            collection.delete_one({"id": book[0]})
            continue

    documents = [{"id": book[0], "content": book[1].decode("utf-8", errors="ignore")} for book in books]

    try:
        result = collection.insert_many(documents)
        print(f"Inserted {len(result.inserted_ids)} documents into the database.")
    except Exception as e:
        print("An error occurred while inserting documents:", e)
