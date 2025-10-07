# test_benchmark_indexer.py
import random
from indexer import process_book, tokenize
from repository_connection import collection
from search_engine import search_mdb  # ✅ deine echte Suchfunktion
from pathlib import Path

# ----------------------
# REPRODUCIBLE SETUP
# ----------------------
SEED = 42
random.seed(SEED)

BOOK_SAMPLE_SIZE = 5
TERM_SAMPLE_SIZE = 10

def get_fixed_books():
    """Deterministische Auswahl von Büchern für reproduzierbare Benchmarks."""
    return list(collection.find({}, {"id": 1, "content": 1}).sort("id", 1).limit(BOOK_SAMPLE_SIZE))

def get_fixed_terms():
    """Extrahiere feste Terms aus den ersten Büchern."""
    books = get_fixed_books()
    terms = []
    for doc in books:
        words = tokenize(doc["content"])
        terms.extend(words)
        if len(terms) >= TERM_SAMPLE_SIZE:
            break
    return terms[:TERM_SAMPLE_SIZE]

# ----------------------
# BENCHMARKS
# ----------------------

def test_indexing_speed(benchmark):
    """
    Benchmark: Wie schnell lassen sich echte Bücher indexieren?
    """
    books = get_fixed_books()

    def run_indexing():
        for doc in books:
            process_book(doc["id"], doc["content"])

    benchmark.pedantic(run_indexing, iterations=3, rounds=5)


def test_tokenization_speed(benchmark):
    """
    Benchmark: Wie schnell arbeitet der Tokenizer?
    """
    doc = get_fixed_books()[0]
    text = doc["content"]

    benchmark.pedantic(tokenize, args=(text,), iterations=100, rounds=10)


def test_search_fs_performance(benchmark):
    """
    Benchmark: Wie schnell liefert die Filesystem-Suche Ergebnisse?
    """
    terms = get_fixed_terms()

    def run_searches():
        for t in terms:
            search_mdb(t)

    benchmark.pedantic(run_searches, iterations=10, rounds=5)
