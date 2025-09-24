import gutenbergpy.textget
import requests
from bs4 import BeautifulSoup

# IMPORTANT INFO: to be able to run this, you need to install bs4, requests, gutenbergpy libraries (pip install ...)

# Since Gutenberg project website protects against scraping,
# we should add more methods to retrieve the data.
# One option is to scrape the id (I think we will need that always)
# and then we can use gutenbergpy or download it all from the archive as said in the website's source code.


# TODO: get from DB, used to download only new items from the source
last_local_id = 0 

def get_book(id, clean):
    # This gets a book by its gutenberg id number
    raw_book = gutenbergpy.textget.get_text_by_id(id) # with headers
    clean_book = gutenbergpy.textget.strip_headers(raw_book) # without headers
    return clean_book if clean else raw_book


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

def get_books(clean = False, id_first = 1, id_last = get_last_released_book_id()):
    books = []
    for id in range(id_first, id_last):
        books.append(get_book(id, clean))
    return books

def get_new_books(clean):
    start = last_local_id
    end = get_last_released_book_id()
    return get_books(clean, start, end)

print(get_books(False, 1, 5))