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
                {"id": book[0], "title": book[1]["title"], "author": book[1]["author"], "release_date": book[1]["release_date"], "language": book[1]["language"], "content": book[1]["content"], "footer": book[1]["footer"]},
                upsert=True  # insert if not exists
            )
        print(f"Inserted/updated {len(books)} documents into the database.")
    except Exception as e:
        print("An error occurred while inserting documents:", e)
        
def search_in_metadata(type, query):
  try:
    if not type or not query:
        raise ValueError("Both 'type' and 'query' must be provided.")

    # Create a case-insensitive regex for partial matches
    mongo_query = {type: {"$regex": query, "$options": "i"}}

    # Return all documents matching the pattern
    results = list(collection.find(mongo_query, {"_id": 0, "id": 1, "title": 1}))
    return results

  except Exception as e:
    print("An error occurred while searching:", e)
