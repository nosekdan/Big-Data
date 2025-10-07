import re
import json
from pathlib import Path
import repository_connection as repo

# ----------------------
# FILESYSTEM INDEX SETUP
# ----------------------
FS_DIR = Path("../database")
FS_DIR.mkdir(parents=True, exist_ok=True)
            
# ----------------------
# FILESYSTEM SEARCH
# ----------------------

def search_mdb(term: str):
    """Return postings for a term if it exists in mongodb index."""
    first_letter = term[0].lower()
    db = repo.client["invertedIndex"]
    collection = db[first_letter]  # Collection for the first letter
    doc = collection.find_one({"term": term})
    if doc:
        return doc["postings"]
    return []
      
if __name__ == "__main__":
    searchType = input("Do you wanna search for:\n1: Title\n2: Author\n3: Language\n4: Term\n")
    match(searchType):
        case "1":
            title = input("Enter title: ").strip().lower()
            repo.connect_to_db()
            results = repo.search_in_metadata("title", title)
            print("Matching books:", results)
        case "2":
            author = input("Enter author: ").strip().lower()
            repo.connect_to_db()
            results =  repo.search_in_metadata("author", author)
            print("Matching books:", results)
        case "3":
            language = input("Enter language: ").strip().lower()
            repo.connect_to_db()
            results =  repo.search_in_metadata("language", language)
            print("Matching books:", results)
        case "4":
            term = input("Enter search term/s: ").strip().lower()
            # mehrere Suchbegriffe trennen (z.B. durch Leerzeichen)
            terms = term.split()
            if terms:
                postings = set(search_mdb(terms[0]))  # Annahme: search_fs gibt eine Liste von Indexen zurück
                # weitere Terme nacheinander schneiden
                for t in terms[1:]:
                    postings &= set(search_mdb(t))  # Schnittmenge bilden

                if postings:
                    print(f"Found in books: {sorted(postings)}")
                else:
                    print("No results found.")
            else:
                print("No input provided.")
            print("🎉 Search complete.")