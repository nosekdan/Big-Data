from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0", serverSelectionTimeoutMS=5000)
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
    try:
        for book in books:
            collection.replace_one(
                {"id": book[0]},  # match by book ID
                {"id": book[0], "header": book[1]["header"], "content": book[1]["content"], "footer": book[1]["footer"]},
                upsert=True  # insert if not exists
            )
        print(f"Inserted/updated {len(books)} documents into the database.")
    except Exception as e:
        print("An error occurred while inserting documents:", e)
