import gutenbergpy.textget
import requests
from bs4 import BeautifulSoup
import repository_connection as repo
from pathlib import Path

# IMPORTANT INFO: to be able to run this, you need to install bs4, requests, gutenbergpy libraries (pip install ...)

# File, storing which books already got indexed
INDEXED_FILE = Path("../database/indexed_books.txt")

# TODO: get from DB, used to download only new items from the source
last_local_id = 0 

def get_book(id):
    # This gets a book by its gutenberg id number
    raw_book = gutenbergpy.textget.get_text_by_id(id) # with headers
    clean_book = gutenbergpy.textget.strip_headers(raw_book) # without headers
    return [id, clean_book]


def get_last_released_book_id():
    search_url = "https://gutenberg.org/ebooks/search/?sort_order=release_date"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find('ul', class_='results')
    link = results.find('li', class_='booklink')
    if link:
        a = link.find('a', class_='link')
        if a and a.has_attr('href'):
            href = a['href']
            id = int(href.replace('/ebooks/', ''))
            return id
    return None

# First id is included, the last one excluded, following the norm
def get_books(id_first = 1, id_last = get_last_released_book_id()):
    books = []
    for id in range(id_first, id_last):
        books.append(get_book(id))
    return books

def get_new_books():
    start = last_local_id
    end = get_last_released_book_id()
    return get_books(start, end)
    
def store_books(id_first, id_last = 0):
    books = get_books(id_first, id_last)
    # connect to db
    repo.connect_to_db()
    # insert to db
    repo.insert_into_db(books)
    INDEXED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEXED_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
        ids = [int(line) for line in lines]
    # filter out all IDs in the range [id_first, id_last)
    ids = [i for i in ids if not (id_first <= i < id_last)]
    
    # write back updated IDs
    with open(INDEXED_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(str(i) for i in ids) + ("\n" if ids else ""))
      

# Testing
# print(get_books(4, 5))
store_books(8, 9)