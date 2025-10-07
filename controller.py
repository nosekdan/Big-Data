import crawler as cr
import indexer as ind
import random

operation = input("Type 1, if you wanna download specific books or 2, if you wanna download random books or 3, if you wanna index all new books: ")
match(operation):
    case "1":
        ids_string = input("Enter the IDs of all the book you wanna download (or a range like 1-10): ").strip().lower()
        if '-' in ids_string:
            id_first, id_last = map(int, ids_string.split('-'))
            print("Downloading books in range", id_first, "to", id_last - 1)
            cr.store_books(id_first, id_last)
            print("Finished downloading books in range", id_first, "to", id_last - 1)
        else:
            ids = [int(id) for id in ids_string.replace(" ", "").split(",")]
            for id in ids:
                print("Downloading book with ID", id)
                cr.store_books(id, id + 1)  # store_books expects a range, so we do id to id+1
            print("Finished downloading books with IDs", ids)
    case "2":
        num_books = int(input("How many random new books do you wanna download? ").strip())
        max_id = 20000  # assuming Gutenberg has books up to this ID
        for _ in range(num_books):
            random_id = random.randint(1, max_id)
            print("Downloading book with ID", random_id)
            cr.store_books(random_id, random_id + 1)
    case "3":
        ind.reindex_all_books()